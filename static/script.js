// Auto-resize textarea
const textarea = document.getElementById('prompt-input');
textarea.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight < 200 ? this.scrollHeight : 200) + 'px';
});

textarea.addEventListener('keypress', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

function clearChat() {
    const stream = document.getElementById('chat-stream');
    stream.innerHTML = `
        <div class="message bot intro-message">
            <div class="avatar-container">
                <div class="avatar bot-avatar"><i class="fa-solid fa-robot"></i></div>
            </div>
            <div class="message-content">
                <p>Welcome to Math-OS. I am a highly advanced neuro-symbolic solver. Choose your model above and ask me any mathematical question.</p>
            </div>
        </div>
    `;
}

function appendMessage(role, htmlContent) {
    const stream = document.getElementById('chat-stream');
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${role}`;
    
    let avatarHtml = '';
    if (role === 'user') {
        avatarHtml = `
            <div class="avatar-container">
                <div class="avatar user-avatar"><i class="fa-solid fa-user"></i></div>
            </div>
        `;
    } else {
        avatarHtml = `
            <div class="avatar-container">
                <div class="avatar bot-avatar"><i class="fa-solid fa-robot"></i></div>
            </div>
        `;
    }

    msgDiv.innerHTML = `
        ${avatarHtml}
        <div class="message-content">
            ${htmlContent}
        </div>
    `;
    
    stream.appendChild(msgDiv);
    stream.scrollTop = stream.scrollHeight;
    
    return msgDiv.querySelector('.message-content');
}

function triggerMathJax(element) {
    if (window.MathJax) {
        MathJax.typesetPromise([element]).catch((err) => console.log(err.message));
    }
}

async function sendMessage() {
    const prompt = textarea.value.trim();
    if (!prompt) return;

    // Reset UI
    textarea.value = '';
    textarea.style.height = 'auto';
    
    // Get Selected Model
    const modelSelect = document.getElementById('model-select');
    const model = modelSelect.value;
    const modelName = modelSelect.options[modelSelect.selectedIndex].text;

    // Append User Message
    appendMessage('user', `<p>${marked.parseInline(prompt)}</p>`);
    triggerMathJax(document.getElementById('chat-stream').lastElementChild);

    // Create Bot Message Container
    const botContentContainer = appendMessage('bot', `<div class="typing-indicator"><i class="fa-solid fa-circle-notch fa-spin"></i> Processing via ${modelName}...</div>`);
    
    if (model === 'ns') {
        await getNeuroSymbolicResponse(prompt, botContentContainer);
    } else if (model === 'web_rag') {
        await getWebRagResponse(prompt, botContentContainer);
    } else {
        await streamResponse(model, prompt, botContentContainer);
    }
}

async function getWebRagResponse(prompt, container) {
    try {
        const startTime = Date.now();
        const response = await fetch(`/api/web_rag`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt: prompt })
        });

        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        
        const reader = response.body.getReader();
        const decoder = new TextDecoder('utf-8');
        
        container.innerHTML = ''; // Clear indicator
        let logContainer = document.createElement('div');
        logContainer.className = 'pipeline-logs';
        container.appendChild(logContainer);

        let resultContainer = document.createElement('div');
        container.appendChild(resultContainer);
        
        let mainText = '';
        let fullText = '';
        let isThinking = false;
        let thinkText = '';
        
        let mainTextContainer = document.createElement('div');
        resultContainer.appendChild(mainTextContainer);
        
        let currentThinkBlock = null;
        let currentThinkContent = null;

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
                        
                        if (data.step) {
                            const stepStr = data.step;
                            if (stepStr.startsWith('PROMPT: ')) {
                                const promptContent = stepStr.replace('PROMPT: ', '');
                                const promptBlock = document.createElement('div');
                                promptBlock.className = 'think-block';
                                promptBlock.style.borderLeftColor = '#A8C7FA';
                                promptBlock.innerHTML = `
                                    <div class="think-header"><i class="fa-solid fa-terminal"></i> <span>Web Search Context</span> <i class="fa-solid fa-chevron-down" style="margin-left:auto; font-size:12px;"></i></div>
                                    <div class="think-content" style="display:none; font-family: monospace; font-size: 11px;">${promptContent}</div>
                                `;
                                promptBlock.querySelector('.think-header').onclick = () => {
                                    const content = promptBlock.querySelector('.think-content');
                                    const isHidden = content.style.display === 'none';
                                    content.style.display = isHidden ? 'block' : 'none';
                                    promptBlock.querySelector('.fa-chevron-down').style.transform = isHidden ? 'rotate(180deg)' : 'rotate(0deg)';
                                };
                                container.insertBefore(promptBlock, resultContainer);
                            } else {
                                const cleanLog = stepStr.replace('LOG: ', '');
                                const stepDiv = document.createElement('div');
                                stepDiv.style.color = '#9AA0A6';
                                stepDiv.style.fontSize = '0.85rem';
                                stepDiv.style.marginBottom = '4px';
                                stepDiv.innerHTML = `<i class="fa-solid fa-angle-right"></i> ${cleanLog}`;
                                logContainer.appendChild(stepDiv);
                            }
                        } else if (data.text) {
                            const token = data.text;
                            fullText += token;

                            if (fullText.includes('<think>') && !isThinking) {
                                isThinking = true;
                                let parts = fullText.split('<think>');
                                mainText = parts[0];
                                fullText = parts[1] || "";
                                
                                if (mainText) {
                                    mainTextContainer.innerHTML = marked.parse(mainText);
                                }

                                currentThinkBlock = document.createElement('div');
                                currentThinkBlock.className = 'think-block';
                                const thinkHeader = document.createElement('div');
                                thinkHeader.className = 'think-header';
                                thinkHeader.innerHTML = '<i class="fa-solid fa-brain"></i> <span>Reasoning</span> <i class="fa-solid fa-chevron-down" style="margin-left:auto; font-size:12px;"></i>';
                                currentThinkContent = document.createElement('div');
                                currentThinkContent.className = 'think-content';
                                
                                thinkHeader.onclick = () => {
                                    const isHidden = currentThinkContent.style.display === 'none';
                                    currentThinkContent.style.display = isHidden ? 'block' : 'none';
                                    thinkHeader.querySelector('.fa-chevron-down').style.transform = isHidden ? 'rotate(180deg)' : 'rotate(0deg)';
                                };
                                
                                currentThinkBlock.appendChild(thinkHeader);
                                currentThinkBlock.appendChild(currentThinkContent);
                                resultContainer.insertBefore(currentThinkBlock, mainTextContainer);
                                
                                thinkText = fullText;
                                currentThinkContent.textContent = thinkText;
                            } else if (fullText.includes('</think>') && isThinking) {
                                isThinking = false;
                                let parts = fullText.split('</think>');
                                thinkText += parts[0];
                                currentThinkContent.textContent = thinkText;
                                currentThinkContent.style.display = 'none';
                                
                                let afterThink = parts[1] || "";
                                mainText += afterThink;
                                mainTextContainer.innerHTML = marked.parse(mainText);
                                fullText = afterThink;
                            } else {
                                if (isThinking) {
                                    thinkText += token;
                                    if (currentThinkContent) currentThinkContent.textContent = thinkText;
                                } else {
                                    mainText += token;
                                    mainTextContainer.innerHTML = marked.parse(mainText);
                                }
                            }
                        } else if (data.done) {
                            const duration = ((Date.now() - startTime) / 1000).toFixed(2);
                            const timeSpan = document.createElement('div');
                            timeSpan.className = 'thinking-time';
                            timeSpan.innerHTML = `<i class="fa-regular fa-clock"></i> Web-RAG completed in ${duration}s`;
                            container.appendChild(timeSpan);
                            triggerMathJax(container);
                        } else if (data.error) {
                            resultContainer.innerHTML = `<p style="color: #ff6b6b;"><i class="fa-solid fa-triangle-exclamation"></i> Error: ${data.error}</p>`;
                        }
                        
                        const stream = document.getElementById('chat-stream');
                        stream.scrollTop = stream.scrollHeight;
                    } catch (e) {}
                }
            }
        }
    } catch (error) {
        console.error('Fetch error:', error);
        container.innerHTML = `<p style="color: #ff6b6b;"><i class="fa-solid fa-triangle-exclamation"></i> Error: ${error.message}</p>`;
    }
}

async function getNeuroSymbolicResponse(prompt, container) {
    try {
        const startTime = Date.now();
        const response = await fetch(`/api/neuro_symbolic`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt: prompt })
        });

        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        
        const reader = response.body.getReader();
        const decoder = new TextDecoder('utf-8');
        
        container.innerHTML = ''; // Clear indicator
        let logContainer = document.createElement('div');
        logContainer.className = 'pipeline-logs';
        container.appendChild(logContainer);

        let resultContainer = document.createElement('div');
        container.appendChild(resultContainer);

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
                        
                        if (data.step) {
                            const stepStr = data.step;
                            if (stepStr.startsWith('THINK: ')) {
                                const thinkContent = stepStr.replace('THINK: ', '');
                                const thinkBlock = document.createElement('div');
                                thinkBlock.className = 'think-block';
                                thinkBlock.innerHTML = `
                                    <div class="think-header"><i class="fa-solid fa-brain"></i> <span>Model Reasoning</span> <i class="fa-solid fa-chevron-down" style="margin-left:auto; font-size:12px;"></i></div>
                                    <div class="think-content" style="display:none;">${thinkContent}</div>
                                `;
                                thinkBlock.querySelector('.think-header').onclick = () => {
                                    const content = thinkBlock.querySelector('.think-content');
                                    const isHidden = content.style.display === 'none';
                                    content.style.display = isHidden ? 'block' : 'none';
                                    thinkBlock.querySelector('.fa-chevron-down').style.transform = isHidden ? 'rotate(180deg)' : 'rotate(0deg)';
                                };
                                container.insertBefore(thinkBlock, resultContainer);
                            } else if (stepStr.startsWith('PROMPT: ')) {
                                const promptContent = stepStr.replace('PROMPT: ', '');
                                const promptBlock = document.createElement('div');
                                promptBlock.className = 'think-block'; // Reusing style for consistency
                                promptBlock.style.borderLeftColor = '#A8C7FA';
                                promptBlock.innerHTML = `
                                    <div class="think-header"><i class="fa-solid fa-terminal"></i> <span>Internal Prompt / Injection</span> <i class="fa-solid fa-chevron-down" style="margin-left:auto; font-size:12px;"></i></div>
                                    <div class="think-content" style="display:none; font-family: monospace; font-size: 11px;">${promptContent}</div>
                                `;
                                promptBlock.querySelector('.think-header').onclick = () => {
                                    const content = promptBlock.querySelector('.think-content');
                                    const isHidden = content.style.display === 'none';
                                    content.style.display = isHidden ? 'block' : 'none';
                                    promptBlock.querySelector('.fa-chevron-down').style.transform = isHidden ? 'rotate(180deg)' : 'rotate(0deg)';
                                };
                                container.insertBefore(promptBlock, resultContainer);
                            } else {
                                // Standard LOG
                                const cleanLog = stepStr.replace('LOG: ', '');
                                const stepDiv = document.createElement('div');
                                stepDiv.style.color = '#9AA0A6';
                                stepDiv.style.fontSize = '0.85rem';
                                stepDiv.style.marginBottom = '4px';
                                stepDiv.innerHTML = `<i class="fa-solid fa-angle-right"></i> ${cleanLog}`;
                                logContainer.appendChild(stepDiv);
                            }
                        } else if (data.final_answer) {
                            resultContainer.innerHTML = marked.parse(data.final_answer);
                            const duration = ((Date.now() - startTime) / 1000).toFixed(2);
                            const timeSpan = document.createElement('div');
                            timeSpan.className = 'thinking-time';
                            timeSpan.innerHTML = `<i class="fa-regular fa-clock"></i> Pipeline finished in ${duration}s`;
                            container.appendChild(timeSpan);
                            triggerMathJax(container);
                        } else if (data.error) {
                            resultContainer.innerHTML = `<p style="color: #ff6b6b;"><i class="fa-solid fa-triangle-exclamation"></i> Error: ${data.error}</p>`;
                        }
                        
                        const stream = document.getElementById('chat-stream');
                        stream.scrollTop = stream.scrollHeight;
                    } catch (e) {}
                }
            }
        }
    } catch (error) {
        console.error('Fetch error:', error);
        container.innerHTML = `<p style="color: #ff6b6b;"><i class="fa-solid fa-triangle-exclamation"></i> Error: ${error.message}</p>`;
    }
}

async function streamResponse(model, prompt, container) {
    try {
        const response = await fetch(`/api/generate/${model}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt: prompt })
        });

        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        const reader = response.body.getReader();
        const decoder = new TextDecoder('utf-8');
        
        let fullText = '';
        let isThinking = false;
        let thinkText = '';
        let mainText = '';

        container.innerHTML = ''; // Clear typing indicator
        
        let mainTextContainer = document.createElement('div');
        container.appendChild(mainTextContainer);
        
        let currentThinkBlock = null;
        let currentThinkContent = null;

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
                            timeSpan.innerHTML = `<i class="fa-regular fa-clock"></i> Generation completed in ${data.time}s`;
                            container.appendChild(timeSpan);
                            triggerMathJax(container); // Final math render
                            continue;
                        }

                        const token = data.text;
                        if (!token) continue;
                        fullText += token;

                        // Handle <think> blocks
                        if (fullText.includes('<think>') && !isThinking) {
                            isThinking = true;
                            let parts = fullText.split('<think>');
                            mainText = parts[0];
                            fullText = parts[1] || "";
                            
                            if (mainText) {
                                mainTextContainer.innerHTML = marked.parse(mainText);
                            }

                            currentThinkBlock = document.createElement('div');
                            currentThinkBlock.className = 'think-block';
                            
                            const thinkHeader = document.createElement('div');
                            thinkHeader.className = 'think-header';
                            thinkHeader.innerHTML = '<i class="fa-solid fa-brain"></i> <span>Reasoning</span> <i class="fa-solid fa-chevron-down" style="margin-left:auto; font-size:12px;"></i>';
                            
                            currentThinkContent = document.createElement('div');
                            currentThinkContent.className = 'think-content';
                            
                            thinkHeader.onclick = () => {
                                const isHidden = currentThinkContent.style.display === 'none';
                                currentThinkContent.style.display = isHidden ? 'block' : 'none';
                                thinkHeader.querySelector('.fa-chevron-down').style.transform = isHidden ? 'rotate(180deg)' : 'rotate(0deg)';
                            };
                            
                            currentThinkBlock.appendChild(thinkHeader);
                            currentThinkBlock.appendChild(currentThinkContent);
                            container.insertBefore(currentThinkBlock, mainTextContainer);
                            
                            thinkText = fullText;
                            currentThinkContent.textContent = thinkText;
                            
                        } else if (fullText.includes('</think>') && isThinking) {
                            isThinking = false;
                            let parts = fullText.split('</think>');
                            thinkText += parts[0];
                            currentThinkContent.textContent = thinkText;
                            
                            // Close the think block visually when done
                            currentThinkContent.style.display = 'none';
                            
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
                        
                        const stream = document.getElementById('chat-stream');
                        stream.scrollTop = stream.scrollHeight;

                    } catch (e) {
                        // ignore JSON parse errors for incomplete chunks
                    }
                }
            }
        }
    } catch (error) {
        console.error('Fetch error:', error);
        container.innerHTML += `<p style="color: #ff6b6b;"><i class="fa-solid fa-triangle-exclamation"></i> Error: ${error.message}</p>`;
    }
}