import './App.css';
import React, { Component }  from 'react';
import AceEditor from "react-ace";

import 'ace-builds/webpack-resolver';
import "ace-builds/src-noconflict/mode-python";
import "ace-builds/src-noconflict/theme-github";
import "ace-builds/src-noconflict/ext-language_tools";

import {Flowdemo} from './components/Flowdemo';
import Header from './components/Header';
import Footer from './components/Footer';

import Sample from "./Data/sample.json"
import ExeVisualization from './components/ExeVisualization';
class App extends Component {
  constructor(props){
    super(props);
    this.state={
      originCode:"",
      pseudoCode:"",
      currentCode:"",
      flowChartCode:"",
      pseudoCodeStatus:false,
      flowChartCodeStatus:false,
      visualizeExecutionStatus:false
    };
    this.samples = Sample.samples
  }

  componentDidMount(){
    
  }

  onsourceCodeChange = (newValue) =>{
    // console.log(newValue)
    this.setState({
      originCode:newValue
    })
  }
  convertCode = () =>{
    console.log("Origin-code:",this.state.originCode);
    let transformText = this.state.originCode.replaceAll("\n","(enter)").replaceAll("\t","(tab)").replaceAll("+","(add)");
    console.log("Transform Text is:", transformText)
    //Convert Code 
    fetch("/dis?code=" + transformText).then(res => res.json()).then(data =>{
      console.log(data);
      this.setState({
        pseudoCode:data.code
      },()=>{
      })
    });
  }

  justifyExecution = () =>{

    console.log("Origin-code:",this.state.originCode);
    let transformText = this.state.originCode.replaceAll("\n","(enter)").replaceAll("\t","(tab)").replaceAll("+","(add)");
    console.log("Transform Text is:", transformText)
    //Convert Code 
    fetch("/flowchart-sample?code=" + transformText).then(res => res.json()).then(data =>{
      console.log(data.code);
      if(data.code){
        this.setState({ flowChartCode:data.code, visualizeExecutionStatus:true})
      }
      
    });
  }
  
  insertSampleCode = (e) =>{
    console.log(e.target.id)
    var sampleCode = this.samples[e.target.id]
    this.setState({
      originCode:sampleCode.code
    })
  }

  // justifyExecution = ()=>{
  //   this.convertFlowChart();
  //   //check whether the code can be run
  //   if(this.state.flowChartCode !== ""){
  //     this.setState({
  //       visualizeExecutionStatus:true
  //     })
  //   }
    
  // }

  backToEditPage = () =>{
    this.setState({visualizeExecutionStatus:false})
  }
  render(){
    return(
      <div className="App bg-dark">
        <Header/>
        {this.state.visualizeExecutionStatus? <ExeVisualization 
          editCode={this.backToEditPage}
          sourceCode = {this.state.originCode} 
          fcCode = {this.state.flowChartCode}/>:
        
        (<div className='container'> 
          <div className='row'>
          <AceEditor
              className="col"
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
              value={this.state.originCode}
                />
          
            <div className='col-4'>
              <button type="button" className="btn btn-warning m-4 pta-btn-text" id="convert-code" onClick={()=>this.convertCode()} style={{minWidth:"200px"}}>Convert to Pseudo-code</button>
              {/* <button type="button" className="btn btn-warning m-4 pta-btn-text" id="convert-fc" onClick={()=>this.convertFlowChart()}style={{minWidth:"200px"}}>Convert to Flowchart</button> */}
              <button type="button" className="btn btn-warning m-4 pta-btn-text" id="execution" onClick={()=>this.justifyExecution()}style={{minWidth:"200px"}}>Visualization Execution</button>
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
            
            <p className='text-left text-light'>Samples</p>
                <div className='row'>
                  {this.samples.map((sample,index)=>(
                    <div id={index} key={index} className='btn btn-warning col m-1 pta-btn-text' onClick={(e)=>{this.insertSampleCode(e)}}>{sample.type}</div>
                  ))}
                </div>
          </div>
        </div>)}
        <Footer/>  
      </div>
    )
  }
}

export default App;
