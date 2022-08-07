import React, { Component } from 'react';
import { Flowdemo } from './Flowdemo';
import AceEditor from "react-ace";

class ExeVisualization extends Component{
    constructor(props){
        super(props);
        this.sourceCodeArray = this.props.sourceCode.split("\n");
        this.fcCode = this.props.fcCode;
        this.defArr = [];
        this.conArr = [];
        this.state = {
            fcCode:this.props.fcCode,
            exeIndex:0,
            defArr:[],
            conArr:[]
        }

        this.flowChartComponent = React.createRef()

    }
    renderFlowchartCode = () =>{
        let arr = Array(this.fcCode.split("\n"))[0];

        //Define the first "\n" in flowchart code. That is the gap between definition and connection
        var gapIndex = arr.indexOf("");

        this.defArr = arr.slice(0,gapIndex);
        this.conArr = arr.slice(gapIndex,arr.length-1);


    }

    renderActiveBlock = (index) =>{
        this.renderFlowchartCode();

        let blockIndex = index + 2; //Skip the st and input
        
        let retrieveDefArr = this.defArr;
        retrieveDefArr[blockIndex] = retrieveDefArr[blockIndex] + "|target";
        let concatFlowChartCodeArr = retrieveDefArr.concat(this.conArr)
        let newFlowChartCode  = concatFlowChartCodeArr.join("\n")
        this.setState({
            fcCode:newFlowChartCode
        },()=>{
            this.flowChartComponent.current.handleCodeChange(this.state.fcCode)
        })
        
    }
    generateCodeTable = () =>{
        var result = []
        for(var i = 0; i < this.sourceCodeArray.length; i++){
            console.log(this.sourceCodeArray[i]);
            var el = <tr className={"visualize-code "+ (this.state.exeIndex === i ? "pta-highlight-code":"")}>{this.sourceCodeArray[i]}</tr>
            result.push(el)
        }
        return(
            <table>
                {result}
            </table>)
    }

    gotoNextLine = () =>{
        this.setState({
            exeIndex:this.state.exeIndex + 1
        })
    }

    gotoLastLine = () =>{
        this.setState({
            exeIndex:this.state.exeIndex - 1
        })
    }

    
    onFocusCode = (e) =>{
        //Get the target code from the original editor
        var pyTargetCode = e.cursor.row
        console.log(pyTargetCode)
        this.renderActiveBlock(pyTargetCode)

      }

    render(){
        return(<div className='container'>
            <div className='row'>  
            <AceEditor
              className="col"
              mode="python"
              theme="github"
              onCursorChange = {(e)=>this.onFocusCode(e)}
              name="PYTHON_CODE"
              editorProps={{
                  $blockScrolling: true,
              }}
              setOptions={{
                // readOnly:true,
                wrapBehavioursEnabled:true
              }}
              value={this.props.sourceCode}
                />
                <div className='col'>
                    {/* <button type="button" className="btn btn-warning m-4 pta-btn-text" id="forward" onClick={()=>this.gotoNextLine()} style={{minWidth:"200px"}}>Next Code</button>
                    <button type="button" className="btn btn-warning m-4 pta-btn-text" id="rewind" onClick={()=>this.gotoLastLine()}style={{minWidth:"200px"}}>Last Code</button> */}
                    <button type="button" className="btn btn-danger m-4 pta-btn-text" id="edit-code" onClick={this.props.editCode}style={{minWidth:"200px"}}>Back to edit code</button>
                </div>
                <div id="canvas" className='bg-light col'>
                    <Flowdemo
                        ref = {this.flowChartComponent}
                        code={this.state.fcCode}
                    /></div>
                </div>
                <footer className='bg-dark' style={{"height":"8em"}}>

                </footer>
            </div>)
    }
}

export default ExeVisualization;