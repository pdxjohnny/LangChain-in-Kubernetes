import React from "react";
import { createChatBotMessage } from "react-chatbot-kit";
import Options from "../components/Options/Options";

const config = {
  botName: "LangChain in K8s DEMO ",
  initialMessages: [createChatBotMessage(`Hello!`)],
  }
export default config;