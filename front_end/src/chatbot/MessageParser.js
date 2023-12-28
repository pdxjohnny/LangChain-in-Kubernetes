class MessageParser {
  constructor(actionProvider) {
    this.actionProvider = actionProvider;
  }

  parse(message) {
    console.log(message);
    const lowercase = message.toLowerCase();

    if (lowercase.includes("rag")) {
      this.actionProvider.setRagState();
    }

    if (lowercase.includes("optimized")) {
      this.actionProvider.setOptimizedState();
    }
    
    if (lowercase.includes("start")) {
      this.actionProvider.startAgain();
    }

    else (this.actionProvider.chatToModel(lowercase));
  }
}

export default MessageParser;

