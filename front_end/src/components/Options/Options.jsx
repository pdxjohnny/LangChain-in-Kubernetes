import React from "react";

import "./Options.css";

const Options = (props) => {
  const options = [
    {
      text: "Use Optimized models",
      handler: props.actionProvider.setOptimizedState,
      id: 1,
    },
    
    { text: "Use RAG", 
      handler: props.actionProvider.setRagState, 
      id: 2 
    },
    
    { text: "Ask to the foundation Model", handler: () => {}, id: 3 },
  ];

  const buttonsMarkup = options.map((option) => (
    <button key={option.id} onClick={option.handler} className="option-button">
      {option.text}
    </button>
  ));

  return <div className="options-container">{buttonsMarkup}</div>;
};

export default Options;