
import React, { Component, RadioButton,Fragment } from 'react';
import {Container, TextField, FormGroup, Button, RadioGroup, Select, 
        MenuItem, Box, FormControl, Radio,FormControlLabel, Grid, Checkbox
} from '@material-ui/core';

import ExpansionPanel from '@material-ui/core/ExpansionPanel';
import ExpansionPanelSummary from '@material-ui/core/ExpansionPanelSummary';
import ExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import Typography from '@material-ui/core/Typography';

 export default class KomunikaciiFields extends Component {
   constructor(props) {
    super(props);
   }
        
        render(){
          if(this.props.display){
          return (
                           <ExpansionPanel expanded={this.props.state.komunikaciipanel=== true} onChange={(e,expanded)=>{this.props.handleChange(e,expanded); this.props.setState({komunikaciipanel:expanded}); }} style={{padding:"5px",backgroundColor:"#eeeeee"}} >
                          <ExpansionPanelSummary
                          expandIcon={<ExpandMoreIcon />}
                          aria-controls="Komunikaciipanel-content"
                          id="Komunikaciipanel"
                          >
                          <Typography >Комунікації</Typography>
                          </ExpansionPanelSummary>
                       <FormGroup id="Komunikacii">
                       <FormControl>
                        <TextField variant="outlined"
                                style={{marginBottom:"7px"}}
                                select
                                error={this.props.touched.voda && Boolean(this.props.errors.voda)}
                                label="Вода"
                                name="voda"
                                id="voda"
                                value={this.props.values.voda}
                                margin={"dense"}
                                onChange={(e)=>{this.props.handleChange(e);
                                 
                                }}

                                placeholder="Виберіть воду"
                                >


                                <MenuItem value={1}>немає</MenuItem>
                                <MenuItem value={2}>Центральна</MenuItem>
                                <MenuItem value={3}>Скважина</MenuItem>
                                <MenuItem value={4}>Криниця</MenuItem>
                            </TextField>
                       </FormControl>
                       <FormControl>
                        <FormControlLabel
                              control={
                                <Checkbox name="gaz"  value={this.props.values.gaz}  onClick={(event)=>{ this.props.setFieldValue("gaz",Boolean(event.target.checked));}}/>
                              }
                              label="Газ"
                            />
                        </FormControl>
                        <FormControl>
                        <FormControlLabel
                              control={
                                <Checkbox name="svitlo" onClick={(event)=>{ this.props.setFieldValue("svitlo",Boolean(event.target.checked));                             
                                }} 
                                  value={this.props.values.svitlo} />
                              }
                              label="Світло"
                            />
                        </FormControl>
                       <FormControl>
                            <TextField hidden={this.props.values.svitlo==false}
                              variant="outlined"
                              label="Потужність, кВт"
                              display="inline"
                              error={this.props.touched.potyzhnist && Boolean(this.props.errors.potyzhnist)}
                              type="number" 
                              name="potyzhnist" 
                              id="potyzhnist" 
                              margin={"dense"}
                              value={this.props.values.potyzhnist}
                              inputProps={{ min: "1", max: "999999999", step: "1" }}
                              pattern='[0-9]{4}'
                              onKeyDown={e => {
                                    if(this.props.values.potyzhnist.length>4) return e.preventDefault();
                                    if(e.key=="+") return e.preventDefault();
                                    if(e.key=="-") return e.preventDefault();
                                    if(e.key=="Enter") return e.preventDefault();
                                    if(e.key=="e") return e.preventDefault();
                                    if(e.key=="m") return e.preventDefault();
                                    if(e.key==".") return e.preventDefault();
                                    if(e.key==",") return e.preventDefault();
                                  }}
                              onChange={(e,v)=>  { if(e.target.value.length<=4){if(e.target.value!="0")this.props.handleChange(e,v);}}}
                            />
                        </FormControl>
                       <FormControl>
                            <TextField variant="outlined"
                                style={{marginBottom:"7px"}}
                                select
                                error={this.props.touched.kanalizacia && Boolean(this.props.errors.kanalizacia)}
                                label="Каналізація"
                                name="kanalizacia"
                                id="kanalizacia"
                                value={this.props.values.kanalizacia}
                                margin={"dense"}
                                onChange={(e)=>{this.props.handleChange(e);
                                 
                                }}

                                placeholder="Каналізація"
                                >


                                <MenuItem value={1}>немає</MenuItem>
                                <MenuItem value={2}>центральна</MenuItem>
                                <MenuItem value={3}>індивідуальна</MenuItem>

                            </TextField>
                       </FormControl>
                       </FormGroup>
                       </ExpansionPanel>
               
            );
           }

           else{
             return null;
           }
        }
   }