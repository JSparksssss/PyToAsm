import './App.css';
import React, { Component }  from 'react';
import AceEditor from "react-ace";

import 'ace-builds/webpack-resolver';
import "ace-builds/src-noconflict/mode-python";
import "ace-builds/src-noconflict/theme-github";
import "ace-builds/src-noconflict/ext-language_tools";


class App extends Component {
  constructor(props){
    super(props);
    this.state={
      originCode:"",
      pseudoCode:"",
      currentCode:""
    };
    
  }

  componentDidMount(){
    
  }

  onsourceCodeChange = (newValue) =>{
    // console.log(newValue)
    this.setState({
      originCode:newValue
    })
  }
  ontargetCodeChange = (newValue)=>{

  }

  convertCode = () =>{
    console.log("Origin-code:",this.state.originCode);
    let transformText = this.state.originCode.replaceAll("\n","(enter)").replaceAll("\t","(tab)").replaceAll("+","(add)");
    console.log("Transform Text is:", transformText)
    //Convert Code 
    fetch("/dis?code=" + transformText).then(res => res.json()).then(data =>{
      console.log(data);
      this.setState({
        pseudoCode:data.code,
      },()=>{
      })
    });
  }

  render(){
    return(
      <div className="App">
        <div className='container'> 
        <div className='row'>
          <div className='col'>Input</div>
          <div className='col'>Options</div>
          <div className='col'>Output</div>
          
        </div>
          <div className='row'>
          <AceEditor
              className='col'
              mode="python"
              theme="github"
              onChange={this.onsourceCodeChange}
              name="PYTHON_CODE"
              editorProps={{
                  $blockScrolling: true,
              }}
              setOptions={{
                wrapBehavioursEnabled:true
              }}
                />
            
            <div className='col'>
              <button type="button" className="btn btn-outline-primary m-4" id="convert-code" onClick={()=>this.convertCode()} style={{minWidth:"200px"}}>Convert to Pseudo-code</button>
              <button type="button" className="btn btn-outline-primary m-4" id="convert-code" style={{minWidth:"200px"}}>Convert to Flowchart</button>
            </div>
            <AceEditor
                className='col'
                      onChange={this.ontargetCodeChange}
                      name="PSEUDO_CODE"
                      editorProps={{
                        $blockScrolling: true,
                      }}
                      setOptions={{
                        wrapBehavioursEnabled:true
                      }}
                      value={this.state.pseudoCode}
                      />
            
          </div>
        </div>
      </div>
    )
  }
}

export default App;
