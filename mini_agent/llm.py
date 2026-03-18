"""
LLM接口实现
"""
from typing import List, Dict, Any, Optional
from openai import AsyncOpenAI
from pydantic import BaseModel
from mini_agent.logging_config import get_logger

logger = get_logger("llm")


class LLMResponse(BaseModel):
    """LLM响应结果"""
    content: Optional[str] = None
    tool_calls: Optional[List[Dict[str, Any]]] = None


class SimpleLLM:
    """简化的LLM接口"""
    
    def __init__(self, api_key: str, model: str = "gpt-4o-mini", base_url: str = "https://ark.cn-beijing.volces.com/api/coding/v3"):
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url=base_url
        )
        self.model = model
    
    async def chat(
        self,
        messages: List[Dict[str, Any]],
        system_prompt: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None
    ) -> LLMResponse:
        """发送聊天请求"""

        logger.info(f"开始调用LLM - model={self.model}, messages={len(messages)}, tools={len(tools) if tools else 0}")
        logger.info(f"请求参数: model={self.model}, temperature=0.7")
        if system_prompt:
            logger.info(f"系统提示词: {system_prompt[:100]}...")

        # 构建消息列表
        chat_messages = []
        
        # 添加系统消息
        if system_prompt:
            chat_messages.append({"role": "system", "content": system_prompt})
        
        # 添加对话历史
        chat_messages.extend(messages)
        
        # 构建请求参数
        request_params = {
            "model": self.model,
            "messages": chat_messages,
            "temperature": 0.7,
        }
        
        # 如果有工具，添加工具调用参数
        if tools:
            request_params["tools"] = tools
            request_params["tool_choice"] = "auto"
        
        try:
            # 调用OpenAI API
            response = await self.client.chat.completions.create(**request_params)
            
            message = response.choices[0].message
            
            # 解析响应
            result = LLMResponse()
            result.content = message.content
            logger.info(f"LLM响应: {result}")
            # 解析工具调用
            if message.tool_calls:
                result.tool_calls = []
                logger.info(f"收到 {len(message.tool_calls)} 个工具调用")
                for tool_call in message.tool_calls:
                    logger.info(f"工具调用: id={tool_call.id}, function={tool_call.function.name}")
                    logger.info(f"工具参数: {tool_call.function.arguments}")
                    result.tool_calls.append({
                        "id": tool_call.id,
                        "type": "function",
                        "function": {
                            "name": tool_call.function.name,
                            "arguments": tool_call.function.arguments
                        }
                    })
            logger.info(f"LLM响应解析完成，返回结果: {result.model_dump_json(ensure_ascii=False, indent=2)}")
            return result
            
        except Exception as e:
            logger.error(f"LLM调用错误: {e}")
            return LLMResponse(content=f"LLM调用失败: {str(e)}")