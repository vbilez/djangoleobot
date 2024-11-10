
import React, { Component, RadioButton,Fragment,useState } from 'react';
import {Container, TextField, FormGroup, Button, RadioGroup, Select, 
        MenuItem, Box, FormControl, Radio,FormControlLabel, Grid, Checkbox
} from '@material-ui/core';
import ExpansionPanel from '@material-ui/core/ExpansionPanel';
import ExpansionPanelSummary from '@material-ui/core/ExpansionPanelSummary';
import ExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import Typography from '@material-ui/core/Typography';
import {Autocomplete} from '@material-ui/lab';
function stringify(obj) {
  let cache = [];
  let str = JSON.stringify(obj, function(key, value) {
    if (typeof value === "object" && value !== null) {
      if (cache.indexOf(value) !== -1) {
        // Circular reference found, discard key
        return;
      }
      // Store value in our collection
      cache.push(value);
    }
    return value;
  });
  cache = null; // reset the cache
  return str;
}
function FocusEnterUnfocus(el){
    const b = document.getElementById(el);
    const inputField = document.getElementById('searchfield');
    inputField.focus();
    // Create a new keyboard event for 'Enter' key
    const enterEvent = new KeyboardEvent('keydown', {
      key: 'Enter',
      code: 'Enter',
      keyCode: 13,
      which: 13,
    });

    // Dispatch the 'Enter' event on the input element
    inputField.dispatchEvent(enterEvent);
    b.focus();

}
 export default class LocationFieldsOn extends Component {
   constructor(props) {
    super(props);
   
   }
        
        render(){
          if(this.props.display){

          return (
              <ExpansionPanel expanded={this.props.state.locationpanel=== true} onChange={(e,expanded)=>{ this.props.setState({locationpanel:expanded}); }} style={{padding:"5px",backgroundColor:"#eeeeee"}} >
                              <ExpansionPanelSummary
                              expandIcon={<ExpandMoreIcon />}
                              aria-controls="Location-content"
                              id="Locationpanel"
                              >
                            <Typography>Локація</Typography>
                          </ExpansionPanelSummary>
                        <FormGroup id="location"> 
           
  
                           

                            <FormControl >
                                <Autocomplete
                                 freeSolo
                                  id="naspunkt"
                                  name="naspunkt"
                                  defaultValue={{"label":"Львів","value":1}}
                                  error={this.props.errors.naspunkt}
                                  getOptionLabel={option => option.label}
                                  renderOption={option => (
                                    <React.Fragment>
                                      {option.label}
                                    </React.Fragment>
                                  )}
                                  options={this.props.options4}
                        
                                  placeholder="Населений пункт"
                         
                                  renderInput={params => (
                                    <TextField {...params} label="Оберіть населений пункт" variant="outlined" fullWidth margin={"dense"} />
                                  )}
                                  

                                  onChange={(o,v)=> {
                                    if(v!==null){
                                    this.props.handleChange(o,v);
                                      
                                
                                    this.props.setFieldValue("naspunkt",v);
                                      this.props.setState({selectedOption4:v.value});
                                      this.props.setState({selectedNaspunkt:v.label});
                                      let addressstr =   v.label + ' '+ 
                                      this.props.state.selectedRayon + ' '+ 
                                      this.props.state.selectedVulica + ' '+ 
                                      this.props.state.selectedBudynok +  
                                      this.props.state.selectedSection;
                                      document.getElementById("searchfield").value= addressstr;
                                      document.getElementById("locationtext").textContent=addressstr;
                                      FocusEnterUnfocus('naspunkt');
                                      
                     
                                    }
                                    else {
                                      this.props.handleChange(o,v);
                                 
                                      this.props.setState({selectedOption4:{}});
                                      this.props.setState({selectedNaspunkt:''})
                                    }
                                                      
                                  }}
                              
                                  >
                               
                                </Autocomplete>
                                </FormControl>
                            <FormControl>
                                <Autocomplete
                                 freeSolo
                                  id="rayon"
                                  name="rayon"
                                  
                                  error={this.props.errors.rayon}
                                  getOptionLabel={option => option.label}
                                  renderOption={option => (
                                    <React.Fragment>
                                      {option.label}
                                    </React.Fragment>
                                  )}
                          
                        
                                  placeholder="Район"
                                  options={this.props.options2}
                                  renderInput={params => (
                                    <TextField {...params}     label="Оберіть район" variant="outlined" fullWidth margin={"dense"} />
                                  )}
                                  

                                  onChange={(o,v)=> {
                                  
                                    if(v!==null){
                                    this.props.handleChange(o,v);
               
                                
                                    
                                      this.props.setState({selectedOption:v.value});
                                             
                                      this.props.setFieldValue("rayon",v.value);  
                                      this.props.setState({selectedRayon:v.label});
                                      let addressstr =   this.props.state.selectedNaspunkt + ' '+ 
                                      v.label + ' '+ 
                                      this.props.state.selectedVulica + ' '+ 
                                      this.props.state.selectedBudynok +  
                                      this.props.state.selectedSection;
                                      document.getElementById("searchfield").value= addressstr;
                                      document.getElementById("locationtext").textContent=addressstr;
                                      FocusEnterUnfocus('rayon');
                                      // this.props.setFieldValue("naspunkt",v);
                                    }
                                    else {
                                      this.props.handleChange(o,v);
                                      this.props.setState({selectedRayon:''});
                                      // this.props.setState({selectedOption:{}});
                                      // this.props.setFieldValue("naspunkt",{});
                                      // this.props.setFieldValue("rayon","");  
                                      // this.props.setFieldValue("vulica","");  
                                    }
                                                      
                                  }}
                              
                                  >
                               
                                </Autocomplete>
                                </FormControl>


                                <FormControl>
                                <Autocomplete
                                 freeSolo
                                  id="vylica"
                                  name="vylica"
                                 
                                  error={this.props.errors.vylica}
                                  getOptionLabel={option => option.label}
                                  renderOption={option => (
                                    <React.Fragment>
                                      {option.label}
                                    </React.Fragment>
                                  )}
                          
                        
                                  placeholder="Вулиця"
                                  options={this.props.filteredOptions}
                                  renderInput={params => (
                                    <TextField {...params}     label="Оберіть вулицю" variant="outlined" fullWidth margin={"dense"} />
                                  )}
                                  

                                  onChange={(o,v)=> {
                                  
                                    if(v!==null){
                                    this.props.handleChange(o,v);
               
                                
                                    
                                      this.props.setState({selectedOption2:v.value});

                                      //document.getElementById("locationtext").textContent= v.label;
                                    
                   
                                      // this.props.setFieldValue("naspunkt",v);
                                      // this.props.setFieldValue("rayon",v.value);  
                                       this.props.setFieldValue("vulica",v.value);  
                                       this.props.setState({selectedVulica:v.label});                          
                                       let addressstr =   this.props.state.selectedNaspunkt + ' '+ 
                                       this.props.state.selectedRayon + ' '+ 
                                       v.label + ' '+ 
                                       this.props.state.selectedBudynok + 
                                       this.props.state.selectedSection;
                                       document.getElementById("searchfield").value= addressstr;
                                       document.getElementById("locationtext").textContent=addressstr;
                                       FocusEnterUnfocus('vylica');
                                    }
                                    else {
                                      this.props.handleChange(o,v);
                                      this.props.setState({selectedVulica:''});
                                      // this.props.setState({selectedOption:{}});
                                      // this.props.setFieldValue("naspunkt",{});
                                      // this.props.setFieldValue("rayon","");  
                                      // this.props.setFieldValue("vulica","");  
                                    }
                                                      
                                  }}
                              
                                  >
                               
                                </Autocomplete>
                                </FormControl>

                                {/* <TextField 
                                  hidden={this.props.values.locationselect==2||this.props.values.locationselect==''}
                                  variant="outlined" 
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
                                            {this.props.filteredOptionsLoc.map(option => (
                                            <MenuItem key={option.value} value={option.value} disabled={option.disabled}>
                                              {option.label}
                                            </MenuItem>
                                          ))} 
                                </TextField>
                                <TextField 
                                  hidden={this.props.values.locationselect==3||this.props.values.locationselect==''}
                                  variant="outlined"
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
                                          
                                          {this.props.filteredOptions3.map(option => (
                                            <MenuItem key={option.value} value={option.value} disabled={option.disabled}>
                                              {option.label}
                                            </MenuItem>
                                          ))} 
                                </TextField>
                                 */}
                       </FormGroup>
                       <FormGroup>
                         <Grid container >
                            <Grid item md={4} xs={4} sm={4}>
                              <TextField variant="outlined"
                                label="Будинок"
                                error={this.props.touched.budynok && Boolean(this.props.errors.budynok)}
                                display="inline"
                                type="text" 
                                name="budynok" 
                                id="budynok" 
                                onChange={(ev)=> {
                                  
                                  this.props.setFieldValue("budynok",ev.target.value);
                                  this.props.setState({selectedBudynok:ev.target.value});
                                  let addressstr =   this.props.state.selectedNaspunkt + ' '+ 
                                  this.props.state.selectedRayon + ' '+ 
                                  this.props.state.selectedVulica + ' '+ 
                                  ev.target.value +  
                                  this.props.state.selectedSection;
                                  document.getElementById("searchfield").value= addressstr;
                                  document.getElementById("locationtext").textContent=addressstr;
                                  
                                  FocusEnterUnfocus('budynok');
                                 
                                }}
                                // onChange={this.props.handleChange}
                                onBlur={this.props.handleBlur}
                                value={this.props.values.budynok}
                                margin={"dense"}

                                style = {{marginRight: "15px"}}
                                inputProps={{
                                  maxLength: 5
                                }}
                              />
                            </Grid>
                            <Grid item  md={4}  xs={4} sm={4} hidden={this.props.state.type==3||this.props.state.type==4||this.props.state.type==6}>
                                <TextField variant="outlined"
                                  label="Секція"
                                  error={this.props.touched.korpus && Boolean(this.props.errors.korpus)}
                                  display="inline"
                                  type="text" 
                                  name="korpus" 
                                  id="korpus" 
 
                                  onChange={(ev)=> {
                                  
                                    this.props.setFieldValue("korpus",ev.target.value);
                                    this.props.setState({selectedSection:ev.target.value});
                                    let addressstr =   this.props.state.selectedNaspunkt + ' '+ 
                                    this.props.state.selectedRayon + ' '+ 
                                    this.props.state.selectedVulica + ' '+ 
                                    this.props.state.selectedBudynok + 
                                    ev.target.value;
                                    document.getElementById("searchfield").value= addressstr;
                                    document.getElementById("locationtext").textContent=addressstr;
                                    
                                    FocusEnterUnfocus('korpus');
                                   
                                  }}
                                  onBlur={this.props.handleBlur}
                                  value={this.props.values.korpus}
                                  margin={"dense"}
                                 
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
                             
                           </Grid>
                           <FormControl>
                            <div id="locationtext"></div>
                           </FormControl>
                         <FormControl>
                         <div id="map"  style={{width:"100%",height: 400}}></div>
                         <input type="text" id="searchfield" placeholder="Введіть локацію" onKeyPress={e => { e.which === 13 && e.preventDefault() }}/>
                         <div id="mapSearchInput"></div>
                         <div id="mapErrorMsg"></div>
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