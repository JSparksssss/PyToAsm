import React, { Component } from 'react';
import { Flowdemo } from './Flowdemo';

class ExeVisualization extends Component{
    constructor(props){
        super(props);
        this.sourceCodeArray = this.props.sourceCode.split("\n");
        this.fcCode = this.props.fcCode;
        this.state = {
            exeIndex:0
        }

    }

    generateCodeTable = () =>{
        var result = []
        for(var i = 0; i < this.sourceCodeArray.length; i++){
            console.log(this.sourceCodeArray[i]);
            var el = <tr className={"visualize-code "+ (this.state.exeIndex === i ? "pta-highlight-code":"")}>  {this.sourceCodeArray[i]}</tr>
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
    
    render(){
        return(<div className='container'>
            <div className='row'>  
                <div className='bg-light col'>
                    {this.generateCodeTable()}
                </div>
                <div className='col'>
                    <button type="button" className="btn btn-warning m-4 pta-btn-text" id="forward" onClick={()=>this.gotoNextLine()} style={{minWidth:"200px"}}>Next Code</button>
                    <button type="button" className="btn btn-warning m-4 pta-btn-text" id="rewind" onClick={()=>this.gotoLastLine()}style={{minWidth:"200px"}}>Last Code</button>
                    <button type="button" className="btn btn-danger m-4 pta-btn-text" id="edit-code" onClick={this.props.editCode}style={{minWidth:"200px"}}>Back to edit code</button>
                </div>
                <div id="canvas" className='bg-light col'>
                    <Flowdemo
                        code={this.fcCode}
                    /></div>
                </div>
            </div>)
    }
}

export default ExeVisualization;