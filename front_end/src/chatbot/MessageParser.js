class MessageParser {
  constructor(actionProvider) {
    this.actionProvider = actionProvider;
  }

  parse(message) {
    console.log(message);
    const lowercase = message.toLowerCase();

    if (lowercase.includes("rag")) {
      this.actionProvider.setRagState();
    } else if (lowercase.includes("optimized")) {
      this.actionProvider.setOptimizedState();
    } else if (lowercase.includes("start")) {
      this.actionProvider.startAgain();
    } else {
      this.actionProvider.chatToModelTrigger(lowercase);
    }
  }
}

export default MessageParser;

