class ActionProvider {
    constructor(createChatBotMessage, setStateFunc) {
      this.createChatBotMessage = createChatBotMessage;
      this.setState = setStateFunc;
    }
  
    greet = () => {
      const message = this.createChatBotMessage("Hello friend.");
      //this.addMessageToState(message);
    };
  
    chatToPython = async (message) => {
      try {
        const sendMessageToAPI = async (message) => {
          try {
            const response = await fetch('http://ec2-54-221-63-234.compute-1.amazonaws.com:5000/ws', {
              method: 'POST',
              headers: {
                'Content-Type': 'text/plain', // Set the appropriate Content-Type
              },
              body:(message), // Format the body as JSON
            });
  
            if (!response.ok) {
              throw new Error('Failed to send message to the API');
            }
  
            const result = await response.text();
            // Assuming the API returns a plain text response
            console.log('Message sent successfully:', result);
            return result;


          } catch (error) {
            console.error('Error sending message to API:', error.message);
          }
        };
  
        // Assuming that sendMessageToAPI is an asynchronous function
        const answer = await sendMessageToAPI(message);
        const chatbotMessage = this.createChatBotMessage(answer);
        this.addMessageToState(chatbotMessage);
      } catch (error) {
        console.error('Error in chatToPython:', error.message);
      }
    };
  
    handleJavascriptQuiz = () => {
      const message = this.createChatBotMessage(
        "Fantastic. Here is your quiz. Good luck!",
        {
          widget: "javascriptQuiz",
        }
      );
  
      this.addMessageToState(message);
    };
  
    addMessageToState = (message) => {
      this.setState((prevState) => ({
        ...prevState,
        messages: [...prevState.messages, message],
      }));
    };
  }
  
  export default ActionProvider;
  
  
  
