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
        this.elseArr = this.renderElseArr(this.props.sourceCode);
        this.state = {
            fcCode:this.props.fcCode,
            exeIndex:0,
            defArr:[],
            conArr:[],
            elseArr:[]
            
        }
        this.flowChartComponent = React.createRef()

    }

    //There are not blocks for else:, we should list all else: indexes for skipping them.
    renderElseArr = (code) =>{
        let elseArr = []
        console.log(code);
        let arr = code.split("\n");
        for(var i = 0; i < arr.length; i++){
            if(arr[i].replace(/\s*/g,"") == "else:"){
                elseArr.push(i);
                console.log(i);
            }
                
        }
        return elseArr
    }
    
    renderFlowchartCode = () =>{
        let arr = this.fcCode.split("\n");

        //Define the first "\n" in flowchart code. That is the gap between definition and connection
        var gapIndex = arr.indexOf("");

        this.defArr = arr.slice(0,gapIndex);
        this.conArr = arr.slice(gapIndex,arr.length-1);
        

    }

    renderActiveBlock = (index) =>{
        this.renderFlowchartCode();

        let blockIndex = index+1; //Skip the st
        
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
        let pyTargetCode = e.cursor.row
        let blockIndex = pyTargetCode

        //Skip all else: 
        for(let i = 0; i < this.elseArr.length; i++){
            if(pyTargetCode > this.elseArr[i]){
                blockIndex = blockIndex - 1
            }
            else if (pyTargetCode == this.elseArr[i]){
                alert("There is not a related block in flowchart.")
            }
        }

        this.renderActiveBlock(blockIndex);
        

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