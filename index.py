import streamlit as st
import requests
import re
import json
import base64

# API 설정
CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models"
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# 모델 선택 옵션
CLAUDE_MODELS = [
    "claude-3-haiku-20240307",
    "claude-3-sonnet-20240229",
    "claude-3-opus-20240229",
    "claude-3-5-sonnet-20240620"
]

GEMINI_MODELS = [
    "gemini-1.5-pro",
    "gemini-1.0-pro",
    "gemini-1.5-pro-exp-0801",
    "gemini-1.5-flash"
]

OPENAI_MODELS = [
    "gpt-4o",
    "gpt-4o-mini",
    "gpt-4",
    "gpt-4-turbo",
    "gpt-3.5-turbo"
]

GROQ_MODELS = [
    "llama2-70b-4096",
    "llama2-70b-4096-32k",
    "llama2-13b-2048-32k",
    "llama2-7b-2048-32k",
    "mixtral-8x7b-32768",
    "gemma-7b-it",
    "llama-3.1-70b-versatile",
    "llama-3.1-8b-instant",
    "llama3-70b-8192",
    "llama3-8b-8192",
    "llama3-groq-70b-8192-tool-use-preview",
    "llama3-groq-8b-8192-tool-use-preview"
]

def call_claude_api(prompt, api_key, model):
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": api_key,
        "anthropic-version": "2023-06-01"
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 4096,
        "temperature": 0.9
    }
    response = requests.post(CLAUDE_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['content'][0]['text']
    else:
        raise Exception(f"Claude API 호출 실패. 상태 코드 {response.status_code}: {response.text}")

def call_gemini_api(prompt, api_key, model):
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.9,
            "topK": 64,
            "topP": 0.95,
            "maxOutputTokens": 4096,
            "responseMimeType": "text/plain"
        }
    }
    url = f"{GEMINI_API_URL}/{model}:generateContent?key={api_key}"
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    else:
        raise Exception(f"Gemini API 호출 실패. 상태 코드 {response.status_code}: {response.text}")

def call_openai_api(prompt, api_key, model):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 4096,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "response_format": {"type": "text"}
    }
    response = requests.post(OPENAI_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        raise Exception(f"OpenAI API 호출 실패. 상태 코드 {response.status_code}: {response.text}")

def call_groq_api(prompt, api_key, model):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 4096,
        "top_p": 1,
        "stream": False,
        "stop": None
    }
    
    # 모델별 특별 설정
    if "32k" in model:
        data["max_tokens"] = 32768
    elif "8192" in model:
        data["max_tokens"] = 8192
    
    response = requests.post(GROQ_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        raise Exception(f"Groq API 호출 실패. 상태 코드 {response.status_code}: {response.text}")

def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{file_label}">다운로드 {file_label}</a>'
    return href

def analyze_and_structure_content(content, api_choice, api_key, model):
    prompt = f"""
1. 다음 내용을 분석하고 4-6개의 주요 포인트나 주제를 식별하세요:
<content>
{content}
</content>

2. 각 주요 포인트에 대해:
   a) 핵심 아이디어를 2-3문장으로 요약하세요.
   b) 관련된 하위 개념이나 세부 사항을 2-3개 나열하세요.
   c) 가능한 경우, 실제 사례나 예시를 1-2개 제공하세요.
   d) 관련된 전문 용어나 중요 개념을 1-2개 포함하세요.
   e) 해당 포인트와 관련된 짧은 인용구, 통계, 또는 팁을 제안하세요.

3. 각 포인트에 대해 200x150 픽셀 크기의 시각적 요소(차트, 다이어그램, 아이콘 등)를 제안하세요. 주제에 따라 적절한 시각화 방법을 선택하세요.

4. 포인트들을 논리적 순서로 배열하고, 각 포인트에 적절한 아이콘이나 심볼을 제안하세요.

5. <thinking> 태그를 사용하여 당신의 구조화 과정과 선택한 시각화 방법에 대한 근거를 설명하세요.

6. 최종 구조를 JSON 형식으로 제공하세요. 이 JSON은 복잡하고 정보가 풍부한 단일 페이지 HTML 슬라이드를 생성하는 데 사용될 것입니다.

목표는 주어진 내용을 바탕으로 포괄적이고 시각적으로 매력적인 슬라이드 구조를 만드는 것입니다. 내용의 복잡성과 깊이에 따라 적절히 조정하세요.
"""
    if api_choice == "Claude":
        return call_claude_api(prompt, api_key, model)
    elif api_choice == "Gemini":
        return call_gemini_api(prompt, api_key, model)
    elif api_choice == "Groq":
        return call_groq_api(prompt, api_key, model)
    else:  # OpenAI
        return call_openai_api(prompt, api_key, model)

def generate_html_infographic(structure_json, api_choice, api_key, model):
    prompt = f"""
1. 다음 JSON 구조를 바탕으로 HTML 슬라이드를 생성하세요:
<json>
{structure_json}
</json>

2. 다음 사양에 따라 HTML 코드를 작성하세요:
   - Tailwind CSS를 스타일링에 사용하세요 (Tailwind CSS CDN 포함)
   - 1200x900 픽셀 크기의 고정 레이아웃으로 설계하세요. 필요한 경우 스크롤 가능하게 만드세요.
   - 에어비엔비 컬러 스타일을 적용하세요.
   - Lucide 아이콘을 적절히 활용하세요
   - 각 섹션에 제안된 시각적 요소(차트, 다이어그램, 아이콘 등)를 포함하세요
   - 내용의 복잡성에 따라 적절한 레이아웃과 디자인 복잡도를 선택하세요

3. 콘텐츠 가이드라인:
   - 주요 포인트를 명확하게 강조하세요
   - 텍스트와 시각적 요소의 균형을 맞추세요
   - 필요한 경우 계층 구조를 사용하여 정보를 조직화하세요
   - 슬라이드의 전체적인 흐름과 가독성을 고려하세요

4. 최종 HTML 코드를 제공하세요. 전체 HTML 코드를 <html_code> 태그 안에 넣으세요.

목표는 주어진 내용을 바탕으로 정보가 풍부하고 시각적으로 매력적인 슬라이드를 생성하는 것입니다. 내용의 성격과 복잡성에 따라 적절히 조정하세요.
"""
    if api_choice == "Claude":
        return call_claude_api(prompt, api_key, model)
    elif api_choice == "Gemini":
        return call_gemini_api(prompt, api_key, model)
    elif api_choice == "Groq":
        return call_groq_api(prompt, api_key, model)
    else:  # OpenAI
        return call_openai_api(prompt, api_key, model)

def clean_html(html_content):
    html_content = re.sub(r'```html\s*', '', html_content)
    html_content = re.sub(r'```\s*$', '', html_content)
    return html_content.strip()

# 예시 텍스트 추가
EXAMPLE_TEXTS = {
    "인공지능의 윤리": """
    인공지능(AI)의 발전은 많은 윤리적 문제를 제기합니다. 주요 관심사로는 프라이버시, 편견, 책임, 투명성이 있습니다.
    AI 시스템은 개인 데이터를 처리하므로 프라이버시 보호가 중요합니다. 또한, AI 알고리즘의 편견은 불공정한 결정을 초래할 수 있습니다.
    AI의 결정에 대한 책임 소재도 명확해야 하며, AI 시스템의 작동 방식에 대한 투명성도 확보되어야 합니다.
    이러한 윤리적 고려사항들을 바탕으로 AI 개발과 사용에 대한 규제와 가이드라인이 필요합니다.
    """,
    "기후 변화와 대응": """
    기후 변화는 전 세계적인 환경 문제로, 지구 온난화, 해수면 상승, 극단적 기상 현상 등을 초래합니다.
    주요 원인으로는 온실가스 배출, 산림 파괴, 산업화가 있습니다. 이에 대한 대응으로 재생 에너지 사용 확대,
    에너지 효율 개선, 산림 보존 등의 정책이 추진되고 있습니다. 개인 차원에서도 에너지 절약,
    재활용, 친환경 제품 사용 등으로 기여할 수 있습니다. 국제적 협력과 정부 정책, 기업의 책임,
    개인의 실천이 모두 중요한 역할을 합니다.
    """,
    "현대 예술의 트렌드": """
    현대 예술은 다양성과 실험성이 특징입니다. 디지털 기술의 발전으로 새로운 매체와 표현 방식이 등장했습니다.
    NFT 아트, 가상현실(VR) 작품 등 기술과 예술의 융합이 두드러집니다. 사회적 이슈를 반영한 작품들도 증가하고 있으며,
    관객 참여형 예술, 환경 예술 등 새로운 형태의 예술도 주목받고 있습니다. 글로벌화로 인해 다양한 문화권의 예술이
    서로 영향을 주고받으며, 전통과 현대의 조화를 추구하는 경향도 있습니다. 예술 시장에서는 온라인 플랫폼의 역할이
    커지고 있으며, 예술의 상업화와 대중화에 대한 논의도 활발합니다.
    """
}

st.title('슬라이드 생성기')

# AI 모델 선택
api_choice = st.selectbox('AI 모델 선택:', ('Claude', 'Gemini', 'OpenAI', 'Groq'))

# 선택된 AI에 따라 모델 옵션 제공
if api_choice == "Claude":
    model = st.selectbox('Claude 모델 선택:', CLAUDE_MODELS)
elif api_choice == "Gemini":
    model = st.selectbox('Gemini 모델 선택:', GEMINI_MODELS)
elif api_choice == "OpenAI":
    model = st.selectbox('OpenAI 모델 선택:', OPENAI_MODELS)
else:  # Groq
    model = st.selectbox('Groq 모델 선택:', GROQ_MODELS)

api_key = st.text_input(f"{api_choice} API 키를 입력하세요:", type="password")

# 예시 텍스트 선택 옵션
content_choice = st.radio(
    "내용 선택:",
    ("직접 입력", "예시 텍스트 사용")
)

if content_choice == "직접 입력":
    content = st.text_area('인포그래픽으로 만들고 싶은 내용을 입력하세요:')
else:
    example_choice = st.selectbox('예시 텍스트 선택:', list(EXAMPLE_TEXTS.keys()))
    content = EXAMPLE_TEXTS[example_choice]
    st.text_area('선택된 예시 텍스트:', content, height=200)

if st.button('생성하기'):
    if content and api_key:
        try:
            with st.spinner('내용 분석 및 구조화 중...'):
                structure_result = analyze_and_structure_content(content, api_choice, api_key, model)
            
            st.subheader('1단계: 내용 분석 및 구조화')
            st.write(structure_result)
            
            structure_json = re.search(r'\{.*\}', structure_result, re.DOTALL)
            if structure_json:
                structure_json = structure_json.group()
                
                with st.spinner('HTML 인포그래픽 생성 중...'):
                    html_result = generate_html_infographic(structure_json, api_choice, api_key, model)
                
                st.subheader('2단계: HTML 인포그래픽 생성')
                html_code = clean_html(html_result)
                st.code(html_code, language='html')
                
                st.components.v1.html(html_code, height=600, scrolling=True)
                
                # HTML 파일 저장 및 다운로드 링크 생성
                with open('infographic.html', 'w', encoding='utf-8') as f:
                    f.write(html_code)
                
                st.markdown(get_binary_file_downloader_html('infographic.html', 'infographic.html'), unsafe_allow_html=True)
            else:
                st.error('구조화된 JSON을 찾을 수 없습니다. 다시 시도해 주세요.')
        except Exception as e:
            st.error(f"오류가 발생했습니다: {str(e)}")
    else:
        st.warning("계속하려면 내용과 API 키를 모두 입력해 주세요.")

st.write(f"참고: 이 애플리케이션은 {api_choice} API의 {model} 모델을 사용합니다. 유효한 API 키를 입력했는지 확인하세요.")
