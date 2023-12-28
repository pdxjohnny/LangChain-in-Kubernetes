class ActionProvider {
  constructor(createChatBotMessage, setState,createClientMessage,state) {
    this.createChatBotMessage = createChatBotMessage;
    this.setState = setState;
    this.state = state;
  }

  // check conditions her 
  chatToModelTrigger =  async (message) => {
    console.log(this.state.rag_mode);
    if (this.state.rag_mode){
      this.chatToRag(message);
    } else if (this.state.opt_model){
      this.chatToRag(message);
    } else {
      // If none of the conditions are met, display a message
      const message = this.createChatBotMessage("Please specify the type of model you want to talk to.");
      this.addMessageToState(message);
    }

  };
  
  chatToRag = async (message) => {
    try {
      console.log('Message sent to RAG');
      console.log(this.state.rag_mode);
      const response = await fetch('http://127.0.0.1:8000/ws', {
        method: 'POST',
        headers: {
          'Content-Type': 'text/plain',
        },
        body: message,
      });

      if (!response.ok) {
        throw new Error('Failed to send message to the API');
      }

      const result = await response.text();
      console.log('Message sent successfully:', result);

      const chatbotMessage = this.createChatBotMessage(result);
      this.addMessageToState(chatbotMessage);
    } catch (error) {
      console.error('Error in chatToPython:', error.message);
    }
  };
  
  setRagState = () => {
    const message = this.createChatBotMessage("Great! Please add your question to the RAG model (Docs were previously updated)");
      this.addMessageToState(message);

    this.setState((prev) => ({
      ...prev,
      rag_mode: true,
      
    }));
  };

  setOptimizedState = () => {
    const message = this.createChatBotMessage("Great! Please add your question to the Optimized Model");
      this.addMessageToState(message);

    this.setState((prev) => ({
      ...prev,
      opt_model: true,
      
    }));
  };

  startAgain = () => {
    const message = this.createChatBotMessage("Great! Let's start again! Let me know to which model you want to talk.");
      this.addMessageToState(message);

    this.setState((prev) => ({
      ...prev,
      rag_mode: false,
      
    }));
    this.setState((prev) => ({
      ...prev,
      opt_model: false,
    }));
  };

  addMessageToState = (message) => {
    this.setState((prevState) => ({
      ...prevState,
      messages: [...prevState.messages, message],
    }));
  };
}

export default ActionProvider;
  
  
  
