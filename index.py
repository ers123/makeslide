import streamlit as st
import requests
import re
import json

# API 설정
CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

def call_claude_api(prompt, api_key):
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": api_key,
        "anthropic-version": "2023-06-01"
    }
    data = {
        "model": "claude-3-5-sonnet-20240620",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 4096,
        "temperature": 0.9
    }
    response = requests.post(CLAUDE_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['content'][0]['text']
    else:
        raise Exception(f"Claude API 호출 실패. 상태 코드 {response.status_code}: {response.text}")

def call_gemini_api(prompt, api_key):
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.9,
            "topK": 64,
            "topP": 0.95,
            "maxOutputTokens": 400000,
            "responseMimeType": "text/plain"
        }
    }
    response = requests.post(f"{GEMINI_API_URL}?key={api_key}", headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    else:
        raise Exception(f"Gemini API 호출 실패. 상태 코드 {response.status_code}: {response.text}")

def call_openai_api(prompt, api_key):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "gpt-4-1106-preview",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    response = requests.post(OPENAI_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        raise Exception(f"OpenAI API 호출 실패. 상태 코드 {response.status_code}: {response.text}")

def analyze_and_structure_content(content, api_choice, api_key):
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
        return call_claude_api(prompt, api_key)
    elif api_choice == "Gemini":
        return call_gemini_api(prompt, api_key)
    else:  # OpenAI
        return call_openai_api(prompt, api_key)

def generate_html_infographic(structure_json, api_choice, api_key):
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
        return call_claude_api(prompt, api_key)
    elif api_choice == "Gemini":
        return call_gemini_api(prompt, api_key)
    else:  # OpenAI
        return call_openai_api(prompt, api_key)

def clean_html(html_content):
    html_content = re.sub(r'```html\s*', '', html_content)
    html_content = re.sub(r'```\s*$', '', html_content)
    return html_content.strip()

st.title('두 단계 프롬프트 인포그래픽 생성기 (다중 API)')

api_choice = st.selectbox('API 선택:', ('Claude', 'Gemini', 'OpenAI GPT'))

api_key = st.text_input(f"{api_choice} API 키를 입력하세요:", type="password")

content = st.text_area('인포그래픽으로 만들고 싶은 내용을 입력하세요:')

if st.button('생성하기'):
    if content and api_key:
        try:
            with st.spinner('내용 분석 및 구조화 중...'):
                structure_result = analyze_and_structure_content(content, api_choice, api_key)
            
            st.subheader('1단계: 내용 분석 및 구조화')
            st.write(structure_result)
            
            structure_json = re.search(r'\{.*\}', structure_result, re.DOTALL)
            if structure_json:
                structure_json = structure_json.group()
                
                with st.spinner('HTML 인포그래픽 생성 중...'):
                    html_result = generate_html_infographic(structure_json, api_choice, api_key)
                
                st.subheader('2단계: HTML 인포그래픽 생성')
                html_code = clean_html(html_result)
                st.code(html_code, language='html')
                
                st.components.v1.html(html_code, height=600, scrolling=True)
            else:
                st.error('구조화된 JSON을 찾을 수 없습니다. 다시 시도해 주세요.')
        except Exception as e:
            st.error(f"오류가 발생했습니다: {str(e)}")
    else:
        st.warning("계속하려면 내용과 API 키를 모두 입력해 주세요.")

st.write(f"참고: 이 애플리케이션은 {api_choice} API를 사용합니다. 유효한 API 키를 입력했는지 확인하세요.")