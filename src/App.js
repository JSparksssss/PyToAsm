import './App.css';
import './global.css';

import React, { Component }  from 'react';
import AceEditor from "react-ace";

import 'ace-builds/webpack-resolver';
import "ace-builds/src-noconflict/mode-python";
import "ace-builds/src-noconflict/theme-github";
import "ace-builds/src-noconflict/ext-language_tools";

import Header from './components/Header';
import Footer from './components/Footer';

import Sample from "./Data/sample.json"
import ExeVisualization from './components/ExeVisualization';

function findLLC(pyIndex,body){
  for(var i = 0; i < body.length; i++){
    if(pyIndex === body[i].py_index){
      return body[i].pseudo_index
  }
  }
  return null 
}

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
      visualizeExecutionStatus:false,
      markers:[],
      py2llcmap:null
    };
    this.samples = Sample.samples
  }

  componentDidMount(){
    
  }

  renderHighlight = (pyIndex) =>{
    this.setState({markers:[]})

    //initialize the Highlight markers
    let markers = []

    //Find the index of low level code
    console.log(this.state.py2llcmap)
    var llc = findLLC(pyIndex,this.state.py2llcmap)

    try{
        for (var i = 0; i < llc.length; i++){
          var index = llc[i]
          markers.push({startRow:index,startCol:0,endRow:index+1,endCol:0,className:"highlight",type:"background"});
        }

        this.setState({markers:markers},()=>{
          console.log(this.state.markers)
        })

    }catch(e){
      console.log(e)
      alert("This pseudo code is not match")
    }
    
    // markers.push({startRow:0,startCol:0,endRow:1,endCol:0,className:"ace_active-line",type:"background"});

    

  }

  onsourceCodeChange = (newValue) =>{
    if(this.state.pseudoCodeStatus === true){
      this.setState({pseudoCodeStatus:false,markers:[]})
    }
    // console.log(newValue)
    this.setState({
      originCode:newValue
    })
  }

  onFocusCode = (e) =>{
    if(this.state.pseudoCodeStatus === true){
      //Get the target code from the original editor
      var pyTargetCode = e.cursor.row
      this.renderHighlight(pyTargetCode)
    }
  }
  whitenOriginCode = (code) =>{
    var codeArr = code.split("\n");
    var whitenArr = [];
    var blankIndex = [];
    var whitenCode = "";
    for (var i = 0; i < codeArr.length; i++){
      let whitenTab = codeArr[i].replaceAll("    ","");
      if (whitenTab == ""){
        blankIndex.push(i);
      }
    }
    for (var i = 0; i < codeArr.length; i++){
      if(blankIndex.indexOf(i) === -1){
        whitenArr.push(codeArr[i]);
      }
    }
    whitenCode = whitenArr.join("\n")
    return whitenCode
  }
  convertCode = () =>{
    console.log("Origin-code:",this.state.originCode);
    let transformText = this.state.originCode.replaceAll("\n","(enter)").replaceAll("\t","(tab)").replaceAll("+","(add)");
    console.log(transformText)
    //Whiten the code for displaying
    let whitenCode = this.whitenOriginCode(this.state.originCode)
    //Convert Code 
    fetch("/dis?code=" + transformText).then(res => res.json()).then(data =>{
      this.setState({
        markers:[],
        originCode:whitenCode,
        pseudoCodeStatus:true,
        pseudoCode:data.code,
        py2llcmap:data.map
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
    var sampleCode = this.samples[e.target.id]
    this.setState({
      pseudoCodeStatus:false,
      pseudoCode:"",
      originCode:sampleCode.code
    })
  }


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
              onCursorChange = {(e)=>this.onFocusCode(e)}
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
                      highlightActiveLine={false}
                      value={this.state.pseudoCode}
                      markers={this.state.markers}
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
