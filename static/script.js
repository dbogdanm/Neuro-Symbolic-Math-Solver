function appendMessage(role, text, containerId) {
    const container = document.getElementById(containerId);
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${role}`;
    
    if (role === 'user') {
        msgDiv.textContent = text;
        container.appendChild(msgDiv);
    } else {
        // Create an empty container for the bot response which will be streamed
        container.appendChild(msgDiv);
        return msgDiv; 
    }
    
    container.scrollTop = container.scrollHeight;
}

async function streamResponse(model, prompt, msgElement, containerId) {
    try {
        const response = await fetch(`/api/generate/${model}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prompt: prompt })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder('utf-8');
        
        let fullText = '';
        let isThinking = false;
        let thinkText = '';
        let mainText = '';

        // UI elements
        let currentThinkBlock = null;
        let currentThinkContent = null;
        let mainTextContainer = document.createElement('div');
        msgElement.appendChild(mainTextContainer);

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            
            const chunk = decoder.decode(value, { stream: true });
            const lines = chunk.split('\n');
            
            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    const dataStr = line.replace('data: ', '').trim();
                    if (!dataStr) continue;
                    
                    try {
                        const data = JSON.parse(dataStr);
                        
                        if (data.done) {
                            const timeSpan = document.createElement('div');
                            timeSpan.className = 'thinking-time';
                            timeSpan.textContent = `Thinking time: ${data.time}s`;
                            msgElement.appendChild(timeSpan);
                            continue;
                        }

                        const token = data.text;
                        if (!token) continue;
                        fullText += token;

                        // Parse <think> tags dynamically
                        if (fullText.includes('<think>') && !isThinking) {
                            isThinking = true;
                            let parts = fullText.split('<think>');
                            mainText = parts[0];
                            fullText = parts[1] || "";
                            
                            if (mainText) {
                                mainTextContainer.innerHTML = marked.parse(mainText);
                            }

                            // Create think block UI
                            currentThinkBlock = document.createElement('div');
                            currentThinkBlock.className = 'think-block';
                            
                            const thinkHeader = document.createElement('div');
                            thinkHeader.className = 'think-header';
                            thinkHeader.innerHTML = '<span>▼ Reasoning</span>';
                            
                            currentThinkContent = document.createElement('div');
                            currentThinkContent.className = 'think-content';
                            
                            thinkHeader.onclick = () => {
                                const isHidden = currentThinkContent.style.display === 'none';
                                currentThinkContent.style.display = isHidden ? 'block' : 'none';
                                thinkHeader.innerHTML = `<span>${isHidden ? '▼' : '▶'} Reasoning</span>`;
                            };
                            
                            currentThinkBlock.appendChild(thinkHeader);
                            currentThinkBlock.appendChild(currentThinkContent);
                            msgElement.insertBefore(currentThinkBlock, mainTextContainer);
                            
                            thinkText = fullText;
                            currentThinkContent.textContent = thinkText;
                            
                        } else if (fullText.includes('</think>') && isThinking) {
                            isThinking = false;
                            let parts = fullText.split('</think>');
                            thinkText += parts[0];
                            currentThinkContent.textContent = thinkText;
                            
                            let afterThink = parts[1] || "";
                            mainText += afterThink;
                            mainTextContainer.innerHTML = marked.parse(mainText);
                            fullText = afterThink; 
                        } else {
                            if (isThinking) {
                                thinkText += token;
                                if (currentThinkContent) {
                                    currentThinkContent.textContent = thinkText;
                                }
                            } else {
                                mainText += token;
                                mainTextContainer.innerHTML = marked.parse(mainText);
                            }
                        }
                        
                        const container = document.getElementById(containerId);
                        container.scrollTop = container.scrollHeight;

                    } catch (e) {
                        console.error('Error parsing JSON:', e, dataStr);
                    }
                }
            }
        }
    } catch (error) {
        console.error('Fetch error:', error);
        msgElement.innerHTML += `<br><span style="color:red">Error: ${error.message}</span>`;
    }
}

function askSingle(model) {
    const input = document.getElementById(`input-${model}`);
    const prompt = input.value.trim();
    if (!prompt) return;

    input.value = '';
    
    // Disable inputs while processing (optional, leaving enabled for now)
    
    const containerId = `chat-history-${model}`;
    appendMessage('user', prompt, containerId);
    
    const botMsgDiv = appendMessage('bot', '', containerId);
    streamResponse(model, prompt, botMsgDiv, containerId);
}

async function getNeuroSymbolicResponse(prompt, msgElement, containerId) {
    try {
        const startTime = Date.now();
        msgElement.innerHTML = "<i>Processing through neuro-symbolic pipeline... This may take a minute.</i>";
        
        const response = await fetch(`/api/neuro_symbolic`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prompt: prompt })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        
        if (data.error) {
            msgElement.innerHTML = `<span style="color:red">Error: ${data.error}</span>`;
            return;
        }
        
        const duration = ((Date.now() - startTime) / 1000).toFixed(2);
        
        // Use marked to parse the response
        msgElement.innerHTML = marked.parse(data.final_answer || "No response generated.");
        
        const timeSpan = document.createElement('div');
        timeSpan.className = 'thinking-time';
        timeSpan.textContent = `Pipeline time: ${duration}s`;
        msgElement.appendChild(timeSpan);
        
        const container = document.getElementById(containerId);
        container.scrollTop = container.scrollHeight;
        
    } catch (error) {
        console.error('Fetch error:', error);
        msgElement.innerHTML = `<span style="color:red">Error: ${error.message}</span>`;
    }
}

function askNeuroSymbolic() {
    const input = document.getElementById(`input-ns`);
    const prompt = input.value.trim();
    if (!prompt) return;

    input.value = '';
    
    const containerId = `chat-history-ns`;
    appendMessage('user', prompt, containerId);
    
    const botMsgDiv = appendMessage('bot', '', containerId);
    getNeuroSymbolicResponse(prompt, botMsgDiv, containerId);
}

function askAll() {
    const globalInput = document.getElementById('input-global');
    const prompt = globalInput.value.trim();
    if (!prompt) return;

    globalInput.value = '';

    // Send to 8B
    const container8b = 'chat-history-8b';
    appendMessage('user', prompt, container8b);
    const botMsg8b = appendMessage('bot', '', container8b);
    streamResponse('8b', prompt, botMsg8b, container8b);

    // Send to 14B
    const container14b = 'chat-history-14b';
    appendMessage('user', prompt, container14b);
    const botMsg14b = appendMessage('bot', '', container14b);
    streamResponse('14b', prompt, botMsg14b, container14b);
    
    // Send to Neuro-Symbolic
    const containerNs = 'chat-history-ns';
    appendMessage('user', prompt, containerNs);
    const botMsgNs = appendMessage('bot', '', containerNs);
    getNeuroSymbolicResponse(prompt, botMsgNs, containerNs);
}

// Allow pressing Enter to send
document.getElementById('input-8b').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') askSingle('8b');
});

document.getElementById('input-14b').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') askSingle('14b');
});

document.getElementById('input-ns').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') askNeuroSymbolic();
});

document.getElementById('input-global').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') askAll();
});
