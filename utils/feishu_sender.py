#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书消息发送工具
用于将消息发送到飞书账号
"""

import json
import requests
import time
from pathlib import Path
from datetime import datetime


class FeishuSender:
    """飞书消息发送类"""

    def __init__(self, config_path="config/feishu_config.json"):
        """初始化飞书发送器"""
        self.config = self._load_config(config_path)
        self.access_token = None
        self.token_expire_time = 0

    def _load_config(self, config_path):
        """加载飞书配置"""
        config_file = Path(config_path)
        if not config_file.exists():
            raise FileNotFoundError(f"配置文件不存在: {config_path}")

        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _get_tenant_access_token(self):
        """获取tenant_access_token"""
        # 如果token还有效,直接返回
        if self.access_token and time.time() < self.token_expire_time:
            return self.access_token

        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        headers = {"Content-Type": "application/json; charset=utf-8"}
        data = {
            "app_id": self.config["app_id"],
            "app_secret": self.config["app_secret"]
        }

        response = requests.post(url, headers=headers, json=data,
                                timeout=self.config["push_settings"]["timeout_seconds"])
        result = response.json()

        if result.get("code") == 0:
            self.access_token = result["tenant_access_token"]
            # token有效期为2小时,提前5分钟过期
            self.token_expire_time = time.time() + result["expire"] - 300
            return self.access_token
        else:
            raise Exception(f"获取access_token失败: {result}")

    def send_text_message(self, content, user_id=None):
        """发送文本消息"""
        if user_id is None:
            user_id = self.config["user_info"]["open_id"]

        token = self._get_tenant_access_token()
        url = "https://open.feishu.cn/open-apis/im/v1/messages"

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8"
        }

        params = {
            "receive_id_type": "open_id"
        }

        data = {
            "receive_id": user_id,
            "msg_type": "text",
            "content": json.dumps({"text": content})
        }

        response = requests.post(url, headers=headers, params=params,
                                json=data,
                                timeout=self.config["push_settings"]["timeout_seconds"])
        return response.json()

    def send_interactive_card(self, title, content, header_color="blue"):
        """发送交互式卡片消息"""
        user_id = self.config["user_info"]["open_id"]
        token = self._get_tenant_access_token()
        url = "https://open.feishu.cn/open-apis/im/v1/messages"

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8"
        }

        params = {
            "receive_id_type": "open_id"
        }

        # 构建卡片内容
        card_content = {
            "config": {
                "wide_screen_mode": True
            },
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": title
                },
                "template": header_color
            },
            "elements": [
                {
                    "tag": "markdown",
                    "content": content
                }
            ]
        }

        data = {
            "receive_id": user_id,
            "msg_type": "interactive",
            "content": json.dumps(card_content)
        }

        response = requests.post(url, headers=headers, params=params,
                                json=data,
                                timeout=self.config["push_settings"]["timeout_seconds"])
        return response.json()

    def send_news_brief(self, news_file_path):
        """发送新闻简报"""
        # 读取新闻文件
        news_file = Path(news_file_path)
        if not news_file.exists():
            raise FileNotFoundError(f"新闻文件不存在: {news_file_path}")

        with open(news_file, 'r', encoding='utf-8') as f:
            news_content = f.read()

        # 提取标题和内容
        lines = news_content.split('\n')
        title = lines[0].replace('# ', '').strip() if lines else "今日新闻简报"

        # 截取前部分内容作为卡片内容(飞书卡片有长度限制)
        # 保留关键摘要部分
        content_lines = []
        for line in lines[1:]:
            if len('\n'.join(content_lines)) > 2800:  # 留一些余量
                content_lines.append("\n...\n\n**完整内容请查看文件**")
                break
            content_lines.append(line)

        content = '\n'.join(content_lines)

        # 发送卡片消息
        header_color = self.config["auto_push_rules"]["news_zhang"]["card_template"]["header_color"]
        result = self.send_interactive_card(title, content, header_color)

        return result


def main():
    """主函数"""
    import sys

    if len(sys.argv) < 2:
        print("使用方法: python feishu_sender.py <news_file_path>")
        print("示例: python feishu_sender.py 2025-11-09/今日新闻.md")
        sys.exit(1)

    news_file = sys.argv[1]

    try:
        sender = FeishuSender()
        print(f"正在发送新闻简报: {news_file}")
        result = sender.send_news_brief(news_file)

        if result.get("code") == 0:
            print("[SUCCESS] 新闻简报发送成功!")
            print(f"消息ID: {result.get('data', {}).get('message_id', 'N/A')}")
        else:
            print(f"[ERROR] 发送失败: {result}")
            sys.exit(1)

    except Exception as e:
        print(f"[ERROR] 发送过程出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
