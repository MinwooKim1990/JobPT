from dataclasses import dataclass, field
from typing import Annotated, Sequence
from langgraph.graph import add_messages
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage


@dataclass
class State:
    session_id: str = ""
    chat_history: list = field(default_factory=list)  # [{"role": "user"|"assistant", "content": str}]
    messages: Annotated[Sequence[AnyMessage], add_messages] = field(default_factory=list)
    agent_name: str = field(default="")
    job_description: str = field(default="")
    resume: str = field(default="")
    company_summary: str = field(default="")
    user_resume: str = field(default="")
    route_decision: str = field(default="")
    company_name: str = field(default="")


# 세션별 State 인스턴스를 저장하는 딕셔너리
session_states = {}


def start_session(session_id: str, **kwargs):
    """새로운 세션 시작 (State 생성, 모든 필드 초기화)"""
    # State의 모든 필드를 kwargs에서 받아서 생성
    state = State(
        session_id=session_id,
        messages=[],
        chat_history=[],
        agent_name=kwargs.get("agent_name", ""),
        job_description=kwargs.get("job_description", ""),
        resume=kwargs.get("resume", ""),
        company_summary=kwargs.get("company_summary", ""),
        user_resume=kwargs.get("user_resume", ""),
        route_decision=kwargs.get("route_decision", ""),
        company_name=kwargs.get("company_name", ""),
    )
    session_states[session_id] = state


def add_user_input_to_state(state, user_input):
    # chat_history에는 기존대로 저장
    state.chat_history.append({"role": "user", "content": user_input})
    # messages에도 HumanMessage로 누적 추가
    state.messages.append(HumanMessage(content=user_input))


def add_assistant_response_to_state(state, assistant_response):
    # chat_history에 assistant 답변 저장
    state.chat_history.append({"role": "assistant", "content": assistant_response})
    # messages에도 AIMessage로 누적 추가
    state.messages.append(AIMessage(content=assistant_response))


def get_session_state(session_id: str, **kwargs):
    """세션의 State 반환 (없으면 새로 생성, 인풋 값으로 초기화)"""
    if session_id not in session_states:
        start_session(session_id, **kwargs)
    return session_states[session_id]


def end_session(session_id: str):
    """세션 종료 및 멀티턴 데이터 삭제"""
    if session_id in session_states:
        del session_states[session_id]
