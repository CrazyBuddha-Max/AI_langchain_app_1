<template>
  <div id="app">
    <h1>CrazyBuddha Chat</h1>
    <div class="chat-container">
      <div v-for="(message, index) in messages" :key="index" class="message">
        <div :class="['message-content', { 'user-message': message.isUser }]" v-html="message.text"></div>
      </div>
    </div>
    <div class="input-container">
      <input v-model="userInput" placeholder="请开始愉快的对话吧！！！" @keyup.enter="sendMessage"/>
      <button @click="sendMessage">发送</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { marked } from 'marked';

export default {
  name: 'App',
  data() {
    return {
      userInput: '', // 用户输入的内容
      messages: [] // 聊天记录
    };
  },
  methods: {
    async sendMessage() {
      // 检查用户输入是否为空
      if (this.userInput.trim() === '') {
        this.messages.push({text: 'Please enter a valid message.', isUser: false});
        return;
      }

      // 将用户消息添加到聊天记录
      this.messages.push({text: this.userInput, isUser: true});

      try {
        // 调用后端接口
        const response = await axios.post('http://aii.cra2y6uddha.fun/generate', null, {
          params: {
            prompt: this.userInput.trim()
          },
          headers: {
            'Content-Type': 'application/json'
          }
        });

        // 将 LLM 的响应添加到聊天记录
         // 将 LLM 的响应解析为 Markdown 并添加到聊天记录
        const markdownText = response.data.result;
        const htmlText = marked(markdownText);
        // console.log(htmlText)
        this.messages.push({text: htmlText, isUser: false});
      } catch (error) {
        console.error('Error calling LLM:', error);

        // 检查错误类型并给出友好的提示
        if (error.response && error.response.status === 422) {
          this.messages.push({text: 'Invalid input. Please try again.', isUser: false});
        } else {
          this.messages.push({text: 'Failed to get response from LLM. Please try again later.', isUser: false});
        }
      }

      // 清空输入框
      this.userInput = '';
    }
  }
};
</script>
<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

.chat-container {
  width: 80%;
  margin: 0 auto;
  border: 1px solid #ccc;
  padding: 10px;
  max-height: 400px;
  overflow-y: auto;
}

.message {
  margin: 10px 0;
}

.message-content {
  padding: 5px 10px;
  border-radius: 5px;
  display: inline-block;
}

.user-message {
  background-color: #007bff;
  color: white;
}

.input-container {
  margin-top: 20px;
}

input {
  width: 70%;
  padding: 10px;
  margin-right: 10px;
}

button {
  padding: 10px 20px;
}
</style>