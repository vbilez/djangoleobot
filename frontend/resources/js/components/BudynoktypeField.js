
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
 export default class BudynoktypeField extends Component {
   constructor(props) {
    super(props);
   }
        
        render(){
          if(this.props.display){
          return (
                        <FormControl>
                       
                            <TextField variant="outlined" required
                                style={{marginBottom:"7px"}}
                                select
                                error={this.props.touched.budynoktype && Boolean(this.props.errors.budynoktype)}
                                label="Тип будинку"
                                name="budynoktype"
                                id="budynoktype"
                                value={this.props.values.budynoktype}
                                margin={"dense"}
                                onChange={(e)=>{this.props.handleChange(e);
   
                                }}

                                placeholder="Виберіть тип будинку"
                                >


                                <MenuItem value={1}>особняк</MenuItem>
                                <MenuItem value={2}>котедж</MenuItem>
                                <MenuItem value={3}>дача</MenuItem>
                                <MenuItem value={4}>незавершене будівництво</MenuItem>
                            </TextField>
                            
                        </FormControl>
               
            );
           }

           else{
             return null;
           }
        }
   }