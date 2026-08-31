#!/usr/bin/env python3
"""
金融分析器 - 基于 MLP 的精准分析工具

功能：
- 获取股票/基金历史数据
- MLP 预测模型分析
- 技术指标计算
- 可视化图表生成
- 投资建议输出
"""

import json
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')

try:
    import yfinance as yf
    YF_AVAILABLE = True
except ImportError:
    YF_AVAILABLE = False

try:
    from sklearn.neural_network import MLPClassifier, MLPRegressor
    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, mean_squared_error
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


class FinancialAnalyzer:
    def __init__(self, symbol: str = "AAPL", period: str = "1y"):
        self.symbol = symbol.upper()
        self.period = period
        self.data = None
        self.scaler = StandardScaler()
        
    def fetch_data(self) -> pd.DataFrame:
        if not YF_AVAILABLE:
            return self._generate_sample_data()
        try:
            ticker = yf.Ticker(self.symbol)
            self.data = ticker.history(period=self.period)
            return self.data
        except Exception as e:
            print(f"获取数据失败: {e}，使用模拟数据")
            return self._generate_sample_data()
    
    def _generate_sample_data(self, days: int = 365) -> pd.DataFrame:
        np.random.seed(42)
        dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
        base_price = 150.0
        prices = [base_price]
        for _ in range(days - 1):
            change = np.random.normal(0, 0.02)
            prices.append(prices[-1] * (1 + change))
        data = pd.DataFrame({
            'Open': prices,
            'High': [p * (1 + abs(np.random.normal(0, 0.01))) for p in prices],
            'Low': [p * (1 - abs(np.random.normal(0, 0.01))) for p in prices],
            'Close': prices,
            'Volume': np.random.randint(1000000, 5000000, days),
        })
        data.index = dates
        return data
    
    def calculate_indicators(self) -> pd.DataFrame:
        if self.data is None:
            self.fetch_data()
        df = self.data.copy()
        df['MA5'] = df['Close'].rolling(5).mean()
        df['MA10'] = df['Close'].rolling(10).mean()
        df['MA20'] = df['Close'].rolling(20).mean()
        df['MA50'] = df['Close'].rolling(50).mean()
        df['MA200'] = df['Close'].rolling(200).mean()
        exp1 = df['Close'].ewm(span=12, adjust=False).mean()
        exp2 = df['Close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = exp1 - exp2
        df['MACD_signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
        df['MACD_hist'] = df['MACD'] - df['MACD_signal']
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        df['BB_middle'] = df['Close'].rolling(20).mean()
        bb_std = df['Close'].rolling(20).std()
        df['BB_upper'] = df['BB_middle'] + (bb_std * 2)
        df['BB_lower'] = df['BB_middle'] - (bb_std * 2)
        df['Return_1d'] = df['Close'].pct_change(1)
        df['Return_5d'] = df['Close'].pct_change(5)
        df['Return_20d'] = df['Close'].pct_change(20)
        df['Volatility_20d'] = df['Return_1d'].rolling(20).std() * np.sqrt(252)
        df['Volume_MA20'] = df['Volume'].rolling(20).mean()
        return df
    
    def prepare_features(self, df: pd.DataFrame) -> pd.DataFrame:
        features = pd.DataFrame({
            'MA5_MA10_ratio': df['MA5'] / df['MA10'],
            'MA10_MA20_ratio': df['MA10'] / df['MA20'],
            'RSI': df['RSI'],
            'MACD': df['MACD'],
            'MACD_hist': df['MACD_hist'],
            'BB_position': (df['Close'] - df['BB_lower']) / (df['BB_upper'] - df['BB_lower']),
            'Volume_ratio': df['Volume'] / df['Volume_MA20'],
            'Return_1d': df['Return_1d'],
            'Return_5d': df['Return_5d'],
            'Volatility_20d': df['Volatility_20d'],
        })
        df['Future_Return_5d'] = df['Close'].shift(-5).pct_change().fillna(0)
        features['Target'] = (df['Future_Return_5d'] > 0).astype(int)
        features.dropna(inplace=True)
        return features
    
    def train_mlp_classifier(self, features: pd.DataFrame) -> Dict:
        if not ML_AVAILABLE or len(features) < 50:
            return {"status": "insufficient_data"}
        X = features.drop('Target', axis=1).values
        y = features['Target'].values
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        mlp = MLPClassifier(hidden_layer_sizes=(64, 32, 16), activation='relu', solver='adam', max_iter=1000, random_state=42, early_stopping=True)
        mlp.fit(X_train_scaled, y_train)
        y_pred = mlp.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        importances = mlp.coefs_[0].mean(axis=0)
        feature_names = list(features.drop('Target', axis=1).columns)
        importance_dict = dict(zip(feature_names, importances))
        return {"accuracy": round(accuracy, 4), "feature_importance": importance_dict}
    
    def train_mlp_regressor(self, features: pd.DataFrame) -> Dict:
        if not ML_AVAILABLE or len(features) < 50:
            return {"status": "insufficient_data"}
        X = features.drop('Target', axis=1).values
        y = features['Future_Return_5d'].values
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        mlp = MLPRegressor(hidden_layer_sizes=(64, 32, 16), activation='relu', solver='adam', max_iter=1000, random_state=42, early_stopping=True)
        mlp.fit(X_train_scaled, y_train)
        y_pred = mlp.predict(X_test_scaled)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        return {"rmse": round(rmse, 6), "expected_return_5d": round(float(y_pred[-1]) * 100, 2)}
    
    def generate_report(self) -> Dict:
        df = self.calculate_indicators()
        features = self.prepare_features(df)
        latest = df.iloc[-1]
        
        report = {
            "symbol": self.symbol,
            "date": str(df.index[-1].date()),
            "price": round(float(latest['Close']), 2),
            "change_1d": round(float(latest['Return_1d'] * 100), 2),
            "change_5d": round(float(latest['Return_5d'] * 100), 2),
            "change_20d": round(float(latest['Return_20d'] * 100), 2),
            "indicators": {
                "RSI": round(float(latest['RSI']), 2),
                "MACD": round(float(latest['MACD']), 4),
                "MACD_signal": round(float(latest['MACD_signal']), 4),
                "BB_position": round(float(latest['BB_position']), 4),
                "volatility_annual": round(float(latest['Volatility_20d']) * 100, 2)
            },
            "ma_system": {
                "MA5": round(float(latest['MA5']), 2),
                "MA10": round(float(latest['MA10']), 2),
                "MA20": round(float(latest['MA20']), 2),
                "MA50": round(float(latest['MA50']), 2)
            },
            "volume": {
                "today": int(latest['Volume']),
                "ratio_to_ma20": round(float(latest['Volume'] / latest['Volume_MA20']), 2) if latest['Volume_MA20'] > 0 else 0
            }
        }
        
        if ML_AVAILABLE and len(features) >= 50:
            clf = self.train_mlp_classifier(features)
            reg = self.train_mlp_regressor(features)
            report["ml_prediction"] = {
                "classifier_accuracy": clf.get("accuracy"),
                "regression_rmse": reg.get("rmse"),
                "expected_5d_return_pct": reg.get("expected_return_5d"),
                "top_features": dict(sorted(clf.get("feature_importance", {}).items(), key=lambda x: x[1], reverse=True)[:5])
            }
        
        report["advice"] = self._generate_advice(report)
        return report
    
    def _generate_advice(self, report: Dict) -> Dict:
        advice = {"signals": [], "risk_level": "中等", "operation": "观望"}
        rsi = report["indicators"]["RSI"]
        macd = report["indicators"]["MACD"]
        macd_sig = report["indicators"]["MACD_signal"]
        bb_pos = report["indicators"]["BB_position"]
        vol = report["indicators"]["volatility_annual"]
        
        if rsi > 70:
            advice["signals"].append({"indicator": "RSI", "status": "超买", "suggestion": "谨慎"})
            advice["risk_level"] = "高"
        elif rsi < 30:
            advice["signals"].append({"indicator": "RSI", "status": "超卖", "suggestion": "关注"})
        else:
            advice["signals"].append({"indicator": "RSI", "status": "正常", "suggestion": "中性"})
        
        advice["signals"].append({"indicator": "MACD", "status": "金叉" if macd > macd_sig else "死叉", "suggestion": "看涨" if macd > macd_sig else "看跌"})
        
        if bb_pos > 0.8:
            advice["signals"].append({"indicator": "布林带", "status": "上轨", "suggestion": "警惕回调"})
        elif bb_pos < 0.2:
            advice["signals"].append({"indicator": "布林带", "status": "下轨", "suggestion": "可能反弹"})
        
        if vol > 50:
            advice["risk_level"] = "高"
        elif vol < 20:
            advice["risk_level"] = "低"
        
        buy_cnt = sum(1 for s in advice["signals"] if "看涨" in s["suggestion"] or "关注" in s["suggestion"])
        sell_cnt = sum(1 for s in advice["signals"] if "看跌" in s["suggestion"] or "谨慎" in s["suggestion"])
        if buy_cnt > sell_cnt:
            advice["operation"] = "买入"
        elif sell_cnt > buy_cnt:
            advice["operation"] = "卖出"
        return advice
    
    def save_report(self, output_path: str = None) -> str:
        report = self.generate_report()
        if output_path is None:
            output_path = f"data/{self.symbol}_analysis_{datetime.now().strftime('%Y%m%d')}.json"
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2, default=str)
        return output_path
    
    def generate_charts(self, output_dir: str = "charts") -> List[str]:
        if not MATPLOTLIB_AVAILABLE:
            return []
        df = self.calculate_indicators()
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        saved = []
        
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(df.index, df['Close'], label='Close', linewidth=1.5)
        ax.plot(df.index, df['MA5'], label='MA5', alpha=0.7)
        ax.plot(df.index, df['MA20'], label='MA20', alpha=0.7)
        ax.fill_between(df.index, df['BB_upper'], df['BB_lower'], alpha=0.1)
        ax.set_title(f'{self.symbol} Price Chart')
        ax.legend()
        ax.grid(True, alpha=0.3)
        p = f"{output_dir}/{self.symbol}_price.png"
        plt.savefig(p, dpi=150, bbox_inches='tight')
        plt.close()
        saved.append(p)
        
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(df.index, df['RSI'], color='blue')
        ax.axhline(70, color='red', linestyle='--')
        ax.axhline(30, color='green', linestyle='--')
        ax.set_title('RSI')
        ax.grid(True, alpha=0.3)
        p = f"{output_dir}/{self.symbol}_rsi.png"
        plt.savefig(p, dpi=150, bbox_inches='tight')
        plt.close()
        saved.append(p)
        
        return saved


def analyze(symbol: str = "AAPL", period: str = "1y") -> Dict:
    analyzer = FinancialAnalyzer(symbol=symbol, period=period)
    return analyzer.generate_report()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Baibai 金融分析器")
    parser.add_argument("symbol", nargs="?", default="AAPL")
    parser.add_argument("--period", default="1y")
    parser.add_argument("--output", default=None)
    parser.add_argument("--charts", action="store_true")
    args = parser.parse_args()
    
    analyzer = FinancialAnalyzer(symbol=args.symbol, period=args.period)
    report = analyzer.generate_report()
    print(json.dumps(report, ensure_ascii=False, indent=2, default=str))
    
    if args.output:
        path = analyzer.save_report(args.output)
        print(f"\n报告已保存: {path}")
    else:
        path = analyzer.save_report()
        print(f"\n报告已保存: {path}")
    
    if args.charts:
        charts = analyzer.generate_charts()
        print(f"\n图表已生成 ({len(charts)} 张)")
