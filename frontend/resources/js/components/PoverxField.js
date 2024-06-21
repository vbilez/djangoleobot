
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
 export default class PoverxField extends Component {
   constructor(props) {
    super(props);
   }
        
        render(){
          if(this.props.display){
          return (
                        <FormControl>
                                <TextField variant="outlined" 
                                    style={{marginBottom:"7px"}}
                                    select
                                    error={this.props.touched.poverx && Boolean(this.props.errors.poverx)}
                                    label="Поверх *"
                                    name="poverx"
                                    id="poverx"
                                    value={this.props.values.poverx}
                                    margin={"dense"}
                                    onChange={(e)=>{this.props.handleChange(e);
                                    
                                    }}

                                    placeholder="Виберіть поверх"
                                    >


                                            {this.props.poverxy.map(option => (
                                            <MenuItem key={option} value={option} >
                                              {option}
                                            </MenuItem>
                                          ))} 
                                </TextField>
                            </FormControl>
               
            );
           }

           else{
             return null;
           }
        }
   }