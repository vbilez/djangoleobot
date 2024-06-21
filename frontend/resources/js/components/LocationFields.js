
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
 export default class LocationFields extends Component {
   constructor(props) {
    super(props);
   }
        
        render(){
          if(this.props.display){
            console.log(this.filteredOptions)
            console.log(this.filteredOptions2)
          return (
              <ExpansionPanel expanded={this.props.state.locationpanel=== true} onChange={(e,expanded)=>{ this.props.setState({locationpanel:expanded}); }} style={{padding:"5px",backgroundColor:"#eeeeee"}} >
                              <ExpansionPanelSummary
                              expandIcon={<ExpandMoreIcon />}
                              aria-controls="Zemlyapanel-content"
                              id="Zemlyapanel"
                              >
                            <Typography>Локація</Typography>
                          </ExpansionPanelSummary>
                        <FormGroup id="location" hidden={this.props.state.type==5}> 
                       <FormGroup>
                       <FormControl>
                            <Select variant="outlined"
                                name="oblast"
                                id="oblast"
                                placeholder="Виберіть область"
                                value={this.props.values.oblast}
                                disabled={true}

                                margin={"dense"}
       
                                >

                                <MenuItem value={0} disabled>Львівська область</MenuItem>
                            </Select>
                            </FormControl>
                            <FormControl >
                                <Autocomplete
                                 freeSolo
                                  id="naspunkt"
                                  name="naspunkt"
                                  
                                  error={this.props.errors.naspunkt}
                                  getOptionLabel={option => option.label}
                                  renderOption={option => (
                                    <React.Fragment>
                                      {option.label}
                                    </React.Fragment>
                                  )}
                          
                        
                                  placeholder="Населений пункт"
                                  options={this.props.options1}
                                  renderInput={params => (
                                    <TextField {...params}     label="Населений пункт" variant="outlined" fullWidth margin={"dense"} />
                                  )}
                                  

                                  onChange={(o,v)=> {
                                  
                                    if(v!==null){
                                    this.props.handleChange(o,v);
               
                                
                                    
                                      this.props.setState({selectedOption:v.value});

                                      this.props.setFieldValue("naspunkt",v);
                                      this.props.setFieldValue("rayon","");  
                                      this.props.setFieldValue("vulica","");  
                                    }
                                    else {
                                      this.props.handleChange(o,v);
                                 
                                      this.props.setState({selectedOption:{}});
                                      this.props.setFieldValue("naspunkt",{});
                                      this.props.setFieldValue("rayon","");  
                                      this.props.setFieldValue("vulica","");  
                                    }
                                                      
                                  }}
                              
                                  >
                               
                                </Autocomplete>
                                </FormControl>
                                <TextField variant="outlined"
                                  select
                                  label="Район"
                                  error={this.props.touched.rayon && Boolean(this.props.errors.rayon)}
                                  name="rayon"
                                  id="rayon"
                                  value={this.props.values.rayon || ''}
                           
                                  // filteredOptions[0]? filteredOptions[0].value : ''
                                  onChange={this.props.handleChange}
                                  placeholder="Район"
                                  margin={"dense"}
                                  >
                                    <MenuItem value="" disabled selected={true}>
                                              Placeholder
                                            </MenuItem>
                                            {this.props.filteredOptions.map(option => (
                                            <MenuItem key={option.value} value={option.value} disabled={option.disabled}>
                                              {option.label}
                                            </MenuItem>
                                          ))} 
                                </TextField>
                                <TextField variant="outlined"
                                  select
                                  label="Вулиця"
                                  error={this.props.touched.vulica && Boolean(this.props.errors.vulica)}
                                  name="vulica"
                                  id="vulica"
                                  value={this.props.values.vulica || ''}
                                  onChange={this.props.handleChange}
                                  placeholder="Вулиця"
                                  margin={"dense"}
                              
                                  >
                                    <MenuItem value="" disabled selected={true}>
                                              Вулиця
                                            </MenuItem>
                                          {this.props.filteredOptions2.map(option => (
                                            <MenuItem key={option.value} value={option.value} disabled={option.disabled}>
                                              {option.label}
                                            </MenuItem>
                                          ))} 
                                </TextField>
                                
                       </FormGroup>
   
                         <Grid container >
                            <Grid item md={4} xs={4} sm={4}>
                              <TextField variant="outlined"
                                label="Будинок"
                                error={this.props.touched.budynok && Boolean(this.props.errors.budynok)}
                                display="inline"
                                type="text" 
                                name="budynok" 
                                id="budynok" 
                                onChange={this.props.handleChange}
                                onBlur={this.props.handleBlur}
                                value={this.props.values.budynok}
                                margin={"dense"}

                                style = {{marginRight: "15px"}}
                                inputProps={{
                                  maxLength: 5
                                }}
                              />
                            </Grid>
                              
                            <Grid item md={4}  xs={4} sm={4} hidden={this.props.state.type==3||this.props.state.type==4||this.props.state.type==6}>
                                <TextField variant="outlined"
                                  label="Кв-ра"
                                  error={this.props.touched.kvartyra && Boolean(this.props.errors.kvartyra)}
                                  display="inline"
                                  type="text" 
                                  name="kvartyra" 
                                  id="kvartyra" 

                                  onChange={this.props.handleChange}
                                  onBlur={this.props.handleBlur}
                                  value={this.props.values.kvartyra}
                                  margin={"dense"}
                                  style = {{marginRight: "15px"}}
                                  inputProps={{
                                    maxLength: 5
                                  }}
                                />
                             </Grid>
                             <Grid item  md={4}  xs={4} sm={4} hidden={this.props.state.type==3||this.props.state.type==4||this.props.state.type==6}>
                                <TextField variant="outlined"
                                  label="Корпус"
                                  error={this.props.touched.korpus && Boolean(this.props.errors.korpus)}
                                  display="inline"
                                  type="text" 
                                  name="korpus" 
                                  id="korpus" 
 
                                  onChange={this.props.handleChange}
                                  onBlur={this.props.handleBlur}
                                  value={this.props.values.korpus}
                                  margin={"dense"}
                                 
                                  inputProps={{
                                    maxLength: 5
                                  }}
                                />
                               </Grid>
                           </Grid>
                       </FormGroup>
            </ExpansionPanel>
            );
           }

           else{
             return null;
           }
        }
   }