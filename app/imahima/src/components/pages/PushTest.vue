<template>
    <div class="container">
      <div>
        <textarea id="chat-log" cols="100" rows="20"></textarea><br>
        <input id="chat-message-input" type="text" size="100"><br>
        <input id="chat-message-submit" type="button" value="Send">
      </div>
      
      <div>
        <button class="btn btn-primary" @click="push">Push!!</button>
      </div>
    </div>
</template>

<script>
export default {
  name: "PushTest",
  mounted: function(){
    // websocket接続(例の単純移植)
    const chatSocket = new WebSocket(
        'ws://'
        + process.env.VUE_APP_API_ENDPOINT_HOST
        + '/ws/chat/'
        + 'pushroom'
        + '/'
    );

    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        document.querySelector('#chat-log').value += (data.message + '\n');
    };

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };

    document.querySelector('#chat-message-input').focus();
    document.querySelector('#chat-message-input').onkeyup = function(e) {
        if (e.keyCode === 13) {  // enter, return
            document.querySelector('#chat-message-submit').click();
        }
    };

    document.querySelector('#chat-message-submit').onclick = function(e) {
        const messageInputDom = document.querySelector('#chat-message-input');
        const message = messageInputDom.value;
        chatSocket.send(JSON.stringify({
            'message': message
        }));
        messageInputDom.value = '';
    };
  },
  methods: {
    push() {
      // this.$push.create('Hello World!')
      this.$push.config({
         serviceWorker: './customServiceWorker.js',
         actions:[
          {action:'act1',title:"ボタンだよ"}
        ]
      });
      this.$push.create("Hello World!",{
        body: "ここはbody",
        icon: '@assets/logo.png',
        timeout: 4000,
        actions:[
          {action:'act1',title:"ボタンだよ"}
        ],
        data:{
          ko: "これってどうなるの？"
        },
        onClick: function (event) {
            window.focus();
            this.close();
            if (event.action === 'act1') {
              // clients.openWindow("/action1");
            }
        }
      })
    }
  }
};
</script>