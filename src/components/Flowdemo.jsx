import React, { Component } from "react";
import Flowchart from "react-simple-flowchart";

export class Flowdemo extends Component {
  constructor(props) {
    super(props);
    const code = `${this.props.code}`;
    const opt = {
      x: 0,
      y: 0,
      "line-width": 3,
      "line-length": 50,
      "text-margin": 10,
      "font-size": 14,
      "font-color": "black",
      "line-color": "black",
      "element-color": "black",
      fill:"white",
      "yes-text": "yes",
      "no-text": "no",
      "arrow-end": "block",
      scale: 1,
      symbols: {
        start: {
          "font-color": "red",
          "element-color": "green",
          "font-weight": "bold"
        },
        end: {
          "font-color": "red",
          "element-color": "green",
          "font-weight": "bold"
        }
      },
      flowstate: {
        target: { fill: "yellow" }
      }
    };

    this.state = {
      code,
      opt,
      elementText: "none"
    };
  }

  handleCodeChange(newCode) {
    this.setState({
      code: newCode
    },()=>{
      console.log(this.state.code);
    });
  }

  handleOptChange(e) {
    this.setState({
      opt: JSON.parse(e.target.value)
    });
  }
  elText(e){
    console.log(e)
  }
  render() {
    const { code, opt, elementText } = this.state;
    return (
        <Flowchart  
            chartCode={code}
            options={opt}
            onClick={(elementText) => this.elText(elementText)}
          />
    );
  }
}
