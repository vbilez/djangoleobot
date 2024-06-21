import React, { Component, RadioButton,Fragment } from 'react';
import {Container, TextField, FormGroup, Button, RadioGroup, Select, 
        MenuItem, Box, FormControl, Radio,FormControlLabel, Grid, Checkbox
} from '@material-ui/core';
import ExpansionPanel from '@material-ui/core/ExpansionPanel';
import ExpansionPanelSummary from '@material-ui/core/ExpansionPanelSummary';
import ExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import Typography from '@material-ui/core/Typography';
import {Autocomplete} from '@material-ui/lab';
import { DatePicker,MuiPickersUtilsProvider } from "@material-ui/pickers";
import DateFnsUtils from '@date-io/date-fns';
import ruLocale from "date-fns/locale/ru";
import InputMask from "react-input-mask";
import ImagesUploadDraggable from "./ImagesUploadDraggable";
 export default class DiliankaFields extends Component {
   constructor(props) {
    super(props);
   }
        
        render(){
          if(this.props.display){
          return (
  <ExpansionPanel expanded={this.props.state.zemlyapanel=== true} onChange={(e,expanded)=>{ this.props.setState({zemlyapanel:expanded}); }} style={{padding:"5px",backgroundColor:"#eeeeee"}} >
                          <ExpansionPanelSummary
                          expandIcon={<ExpandMoreIcon />}
                          aria-controls="Zemlyapanel-content"
                          id="Zemlyapanel"
                          >
                          <Typography>Ділянка</Typography>
                          </ExpansionPanelSummary>
                        <FormGroup>
                        <InputMask mask="9999999999:99:999:9999"  value={this.props.values.kadastrovyi} onChange={this.props.handleChange}  onBlur={this.props.handleBlur}>
                          <TextField variant="outlined"
                            label="Кадастровий номер"
                            error={this.props.touched.kadastrovyi && Boolean(this.props.errors.kadastrovyi)}
                            name="kadastrovyi"
                            id="kadastrovyi"
                            margin={"dense"}

                          >
                          </TextField>
                        </InputMask>
             
                      
                
                        <FormControl>
                             <TextField variant="outlined"
                                style={{marginBottom:"7px"}}
                                select
                                error={this.props.touched.korystuvannia && Boolean(this.props.errors.korystuvannia)}
                                label="Власність"
                                name="korystuvannia"
                                id="korystuvannia"
                                value={this.props.values.korystuvannia}
                                margin={"dense"}
                                onChange={(e)=>{this.props.handleChange(e);}}

                                placeholder="Виберіть користування"
                                >


                                <MenuItem value={1}>Приватна власність</MenuItem>
                                <MenuItem value={2}>Оренда</MenuItem>
                                <MenuItem value={3}>Постійне користування</MenuItem>
                                <MenuItem value={4}>Неоформлена</MenuItem>

                            </TextField>
                            
                        </FormControl>
               

                  
                       <FormControl>
                          
                          <TextField
                              variant="outlined"
                              label="Площа ділянки, сот"
                              display="inline"
                              error={this.props.touched.area_earth && Boolean(this.props.errors.area_earth)}
                              onKeyDown={e => {
                                    if(this.props.values.area_earth.length>9) return e.preventDefault();
                                    if(e.key=="+") return e.preventDefault();
                                    if(e.key=="-") return e.preventDefault();
                                    if(e.key=="Enter") return e.preventDefault();
                                    if(e.key=="e") return e.preventDefault();
                                    if(e.key=="m") return e.preventDefault();
                                    if( e.key=="2" || e.key=="3" || e.key=="4" || e.key=="5" || e.key=="6" || e.key=="7" || e.key=="8" || e.key=="9" || e.key=="1" || e.key=="0") 
                                    {
                                        if(this.props.values.area_earth.toString().indexOf(".")>-1)
                                        {
                                            let index1 = this.props.values.area_earth.toString().indexOf(".");
                                            let str1 = this.props.values.area_earth.toString().slice(index1,this.props.values.area_earth.toString().length );
                                            if(str1.length>2) return e.preventDefault();
                                        }
                                     
                                    } 
                                  }}
                              onChange={(e,v)=>  { 
                                if(!Number(e.target.value)&& e.target.value.length>=1 
                                && e.target.value!="1" 
                                && e.target.value!="2"
                                && e.target.value!="3"
                                && e.target.value!="4"
                                && e.target.value!="5"
                                && e.target.value!="6"
                                && e.target.value!="7"
                                && e.target.value!="8"
                                && e.target.value!="9"
                                ) return;
                                 if(e.target.value.length<=9){
                                        if(e.target.value!="0")this.props.handleChange(e,v);
                                    }
                                }}
                              value={this.props.values.area_earth}  
                              onBlur={this.props.handleBlur}
                              type="text" 
                              name="area_earth" 
                              id="area_earth" 
                              margin={"dense"}
                            />
                          
                        </FormControl>
                        <FormControl>
                       
                            <TextField variant="outlined"
                                style={{marginBottom:"7px"}}
                                select
                                error={this.props.touched.pryznachennia && Boolean(this.props.errors.pryznachennia)}
                                label="Призначення ділянки"
                                name="pryznachennia"
                                id="pryznachennia"
                                value={this.props.values.pryznachennia}
                                margin={"dense"}
                                onChange={(e)=>{this.props.handleChange(e);
                                 
                                }}

                                placeholder="Виберіть призначення"
                                >


                                <MenuItem value={1}>Будівництво квартирних будинків</MenuItem>
                                <MenuItem value={2}>Особиста житлова забудова</MenuItem>
                                <MenuItem value={3}>Садівництво</MenuItem>
                                <MenuItem value={4}>Відпочинок та здоров'я</MenuItem>
                                <MenuItem value={5}>ОСГ</MenuItem>
                                <MenuItem value={6}>Торгівля(комерційна)</MenuItem>
                                <MenuItem value={7}>Промисловість</MenuItem>
                                <MenuItem value={8}>Інше</MenuItem>
                            </TextField>
                            
                        </FormControl>
                        <FormControl>
                       
                            <TextField variant="outlined"
                                style={{marginBottom:"7px"}}
                                select
                                error={this.props.touched.dojizd && Boolean(this.props.errors.dojizd)}
                                label="Доїзд до ділянки"
                                name="dojizd"
                                id="dojizd"
                                value={this.props.values.dojizd}
                                margin={"dense"}
                                onChange={(e)=>{this.props.handleChange(e);
                                 
                                }}

                                placeholder="Доїзд до ділянки"
                                >


                                <MenuItem value={1}>Грунт</MenuItem>
                                <MenuItem value={2}>Бруківка</MenuItem>
                                <MenuItem value={3}>Асфальт</MenuItem>
                                <MenuItem value={4}>відсутній</MenuItem>
                            </TextField>
                            
                        </FormControl>

                        <FormControl>
                         
                          <TextField
                              variant="outlined"
                              label="Опис ділянки"
                              display="inline"
                              error={this.props.touched.opys_earth && Boolean(this.props.errors.opys_earth)}
                              type="text" 
                              name="opys_earth" 
                              id="opys_earth" 
                               multiline   
                               margin={"dense"}
                              
                            />

                        </FormControl>

                        <ImagesUploadDraggable display={true} setState={this.props.setState} imgcount={8} statename={"photozemlia"} caption={"Фото схем ділянки"}/>
                      </FormGroup>
                       </ExpansionPanel>
            );
           }

           else{
             return null;
           }
        }
   }