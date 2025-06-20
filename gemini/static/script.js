async function askQuestion() {
    const input = document.getElementById('questionInput');
    const question = input.value.trim();
    if (!question) return;
    addMessage(question, 'user');
    input.value = '';
    try {
        const response = await fetch('/api/recommend', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question: question })
        });
        const data = await response.json();
        if (response.ok) {
            addMessage(data.recommendation, 'bot');
        } else {
            addMessage('Sorry, an error occurred: ' + data.error, 'bot');
        }
    } catch (error) {
        addMessage('Network error, please try again later.', 'bot');
    }
}

function addMessage(text, type) {
    const container = document.getElementById('chatContainer');
    const message = document.createElement('div');
    message.className = `message ${type}-message`;
    if (type === 'bot') {
        message.innerHTML = formatBotMessage(text);
    } else {
        message.textContent = text;
    }
    container.appendChild(message);
    container.scrollTop = container.scrollHeight;
}

function formatBotMessage(text) {
    // 支持基础 Markdown 排版
    return text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // 粗体
        .replace(/\*(.*?)\*/g, '<em>$1</em>') // 斜体
        .replace(/\n\n/g, '</p><p>') // 段落
        .replace(/\n/g, '<br>') // 换行
        .replace(/\* (.*?)(?=<br>|$)/g, '<li>$1</li>') // 列表
        .replace(/<p>(<li>.*?<\/li>)<\/p>/g, '<ul>$1</ul>') // 列表包裹
        .replace(/^/, '<p>')
        .replace(/$/, '</p>');
}

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        askQuestion();
    }
}

function askSuggestion(question) {
    const input = document.getElementById('questionInput');
    input.value = question;
    askQuestion();
} 