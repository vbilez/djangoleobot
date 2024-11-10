
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
import BudynoktypeField from "./BudynoktypeField";
import BudivliatypeField from "./BudivliatypeField";
import ImagesUploadDraggable from "./ImagesUploadDraggable";
 export default class BudivliaFields extends Component {
   constructor(props) {
    super(props);
   }
        
        render(){
          if(this.props.display){
          return (
 <ExpansionPanel expanded={this.props.state.budivliapanel=== true} onChange={(e,expanded)=>{ this.props.setState({budivliapanel:expanded}); }} style={{padding:"5px",backgroundColor:"#eeeeee"}} >
                          <ExpansionPanelSummary
                          expandIcon={<ExpandMoreIcon />}
                          aria-controls="Budivliapanel-content"
                          id="Budivliapanel"
                          >
                          <Typography >Будівля</Typography>
                          </ExpansionPanelSummary>
                                  <FormGroup>
                         
                        <BudivliatypeField handleChange={this.props.handleChange} values={this.props.values} touched={this.props.touched} errors={this.props.errors} 
                            display={this.props.state.type!=3}
                        />
                        <BudynoktypeField handleChange={this.props.handleChange} values={this.props.values} touched={this.props.touched} errors={this.props.errors} 
                            display={this.props.state.type==3}
                        />
                            <FormControl>
                                <TextField  required variant="outlined"
                                    style={{marginBottom:"7px"}}
                                    select
                                    error={this.props.touched.kstpoverxiv && Boolean(this.props.errors.kstpoverxiv)}
                                    label="Кількість поверхів"
                                    name="kstpoverxiv"
                                    id="kstpoverxiv"
                                    value={this.props.values.kstpoverxiv}
                                    margin={"dense"}
                                    onChange={(e)=>{this.props.handleChange(e);
                                    
                                    }}

                                    placeholder="Виберіть поверх"
                                    >


                                            {this.props.kistpoverxiv.map(option => (
                                            <MenuItem key={option} value={option} >
                                              {option}
                                            </MenuItem>
                                          ))} 
                                </TextField>
                            </FormControl>
                            <FormControl>
                                <TextField  required variant="outlined"
                                    style={{marginBottom:"7px"}}
                                    select
                                    error={this.props.touched.matstin && Boolean(this.props.errors.matstin)}
                                    label="Матеріал стін"
                                    name="matstin"
                                    id="matstin"
                                    value={this.props.values.matstin}
                                    margin={"dense"}
                                    onChange={(e)=>{this.props.handleChange(e);
          
                                    }}

                                    placeholder="Виберіть матеріал стін"
                                    >


                                    <MenuItem value={1}>цегла</MenuItem>
                                    <MenuItem value={2}>панель</MenuItem>
                                    <MenuItem value={3}>газоблок</MenuItem>
                                    <MenuItem value={4}>піноблок</MenuItem>
                                    <MenuItem value={5}>метал</MenuItem>
                                    <MenuItem value={6}>дерево</MenuItem>
                                </TextField>
                            </FormControl>
                            <FormControl>
                                <TextField variant="outlined"
                                    style={{marginBottom:"7px"}}
                                    select
                                    error={this.props.touched.matperekrytya && Boolean(this.props.errors.matperekrytya)}
                                    label="Матеріал перекриття"
                                    name="matperekrytya"
                                    id="matperekrytya"
                                    value={this.props.values.matperekrytya}
                                    margin={"dense"}
                                    onChange={(e)=>{this.props.handleChange(e);
          
                                    }}

                                    placeholder="Виберіть матеріал перекриття"
                                    >
                                    <MenuItem value={1}>з/б</MenuItem>
                                    <MenuItem value={2}>дерево</MenuItem>
                                    <MenuItem value={3}>комбіноване</MenuItem>
                                </TextField>
                            </FormControl>
                            <FormControl>
                                <TextField variant="outlined"
                                    style={{marginBottom:"7px"}}
                                    select
                                    error={this.props.touched.matsxodiv && Boolean(this.props.errors.matsxodiv)}
                                    label="Матеріал сходів"
                                    name="matsxodiv"
                                    id="matsxodiv"
                                    value={this.props.values.matsxodiv}
                                    margin={"dense"}
                                    onChange={(e)=>{this.props.handleChange(e);
          
                                    }}

                                    placeholder="Виберіть матеріал сходів"
                                    >
                                <MenuItem value={1}>дерево</MenuItem>
                                <MenuItem value={2}>бетон</MenuItem>
                                </TextField>
                            </FormControl>
                            <FormControl>
                                <TextField  variant="outlined"
                                    style={{marginBottom:"7px"}}
                                    select
                                    error={this.props.touched.pamyatkarx && Boolean(this.props.errors.pamyatkarx)}
                                    label="Памятка архітектури"
                                    name="pamyatkarx"
                                    id="pamyatkarx"
                                    value={this.props.values.pamyatkarx}
                                    margin={"dense"}
                                    onChange={(e)=>{this.props.handleChange(e);
          
                                    }}

                                    placeholder="Виберіть памятку"
                                    >


                                    <MenuItem value={1}>ні</MenuItem>
                                    <MenuItem value={2}>національного значення</MenuItem>
                                    <MenuItem value={3}>місцевого значення</MenuItem>
                                    <MenuItem value={4}>історичний ареал</MenuItem>
                                </TextField>
                            </FormControl>
                            <FormControl>
                              <MuiPickersUtilsProvider utils={DateFnsUtils} locale={ruLocale}>
                              <DatePicker
                                inputVariant="outlined"
                                openTo="year"
                                format="yyyy"
                                label="Рік будівництва"
                                views={["year"]}
                                value={this.props.values.databudivnyctva}
                                onChange={(e)=>{console.log(e);this.props.setFieldValue("databudivnyctva",e,false);}}
                                margin={"dense"}
                                name="databudivnyctva"
                              />
                            </MuiPickersUtilsProvider>
                            </FormControl>

                           
                                       <FormGroup hidden={this.props.values.budivliatype!==1}> 
                                        <FormControl>
                                        <TextField variant="outlined"
                                          style={{marginBottom:"7px"}}
                                          select
                                          error={this.props.touched.zdachiakvartal && Boolean(this.props.errors.zdachiakvartal)}
                                          label="Здача"
                                          name="zdachiakvartal"
                                          id="zdachiakvartal"
                                          value={this.props.values.zdachiakvartal}
                                          margin={"dense"}
                                          onChange={(e)=>{this.props.handleChange(e);
                                          
                                          }}

                                          placeholder="Здача, квартал"
                                          >
                                          <MenuItem value={1}>I квартал</MenuItem>
                                          <MenuItem value={2}>II квартал</MenuItem>
                                          <MenuItem value={3}>III квартал</MenuItem>
                                          <MenuItem value={4}>IV квартал</MenuItem>
                                        </TextField>
                                      </FormControl>
                                    <FormControl>
                                        <Autocomplete
                                          freeSolo
                                          id="zk"
                                          name="zk"
                                          error={this.props.errors.zk}
                                          getOptionLabel={option => typeof option === 'object' ? option.label : option}
                                          placeholder="ЖК"
                                          options={this.props.zkoptions}
                                          renderInput={params => (
                                            <TextField {...params}     label="ЖК" variant="outlined" fullWidth margin={"dense"} />
                                          )}
                                          renderOption={option => (
                                            <React.Fragment>
                                              {typeof option === 'object' ? option.label : option}
                                            </React.Fragment>
                                          )}

                                 
                                          onChange={(o,v)=> {
                                            this.props.setFieldValue("zk",v);
                                          }}
                                          >
                                      
                                        </Autocomplete>
                                      </FormControl>
                                    
                                  <FormControl>
                    
                              <TextField variant="outlined"
                                  label="Черга будівництва"
                                
                                  error={this.props.touched.chergabudivnyctva && Boolean(this.props.errors.chergabudivnyctva)}
                                  type="number"
                                  name="chergabudivnyctva" 
                                  id="chergabudivnyctva" 
   
                                  min={1}
                                  margin={"dense"}
                                  value={this.props.values.chergabudivnyctva}
                      
                                  onBlur={this.props.handleBlur}
                                  inputProps={{ min: "1", max: "999999999", step: "1" }}
                                  onKeyDown={e => {
                                    if(this.props.values.cina.length>4) return e.preventDefault();
                                    if(e.key=="+") return e.preventDefault();
                                    if(e.key=="-") return e.preventDefault();
                                    if(e.key=="Enter") return e.preventDefault();
                                    if(e.key=="e") return e.preventDefault();
                                    if(e.key=="m") return e.preventDefault();
                                    if(e.key==".") return e.preventDefault();
                                    if(e.key==",") return e.preventDefault();
                                  }}

                                  onChange={(e,v)=>  { if(e.target.value.length<=9){if(e.target.value!="0")this.props.handleChange(e,v);}}} 
                              />
                           
                            </FormControl>

                                      <FormControl>
                                        <TextField variant="outlined"
                                          style={{marginBottom:"7px"}}
                                          select
                                          error={this.props.touched.stanbudivnuctva && Boolean(this.props.errors.stanbudivnuctva)}
                                          label="Стан будівництва"
                                          name="stanbudivnuctva"
                                          id="stanbudivnuctva"
                                          value={this.props.values.stanbudivnuctva}
                                          margin={"dense"}
                                          onChange={(e)=>{this.props.handleChange(e);}}
                                          placeholder="Виберіть стан будівництва"
                                          >
                                          <MenuItem value={1}>будується</MenuItem>
                                          <MenuItem value={2}>збудований первинний</MenuItem>
                                          <MenuItem value={3}>зданий в експлуатацію</MenuItem>
                                          <MenuItem value={4}>заселений</MenuItem>
                                        </TextField>
                                      </FormControl>
                                      <FormControl>
                                        <Autocomplete
                                          freeSolo
                                          id="zabudovnuk"
                                          name="zabudovnuk"
                                          error={this.props.errors.zabudovnuk}
                                          getOptionLabel={option => typeof option === 'object' ? option.label : option}
                                          placeholder="Забудовник"
                                          options={this.props.zabudovnukoptions}
                                          renderInput={params => (
                                            <TextField {...params}     label="Забудовник" variant="outlined" fullWidth margin={"dense"} />
                                          )}
                                          renderOption={option => (
                                            <React.Fragment>
                                              {typeof option === 'object' ? option.label : option}
                                            </React.Fragment>
                                          )}
                                          onChange={(o,v)=> {
                                            this.props.setFieldValue("zabudovnuk",v);
                                          }}
                                          >
                                        </Autocomplete>
                                      </FormControl>
                                      </FormGroup>
                            <FormControl>
                            <TextField
                                variant="outlined"
                                label="Про будівлю"
                                display="inline"
                                error={this.props.touched.probudivliu && Boolean(this.props.errors.probudivliu)}
                                type="text" 
                                name="probudivliu" 
                                id="probudivliu" 
                                  multiline   
                                  margin={"dense"}
                                
                              />
                              </FormControl>
                              <FormControl>
                              <FormControlLabel
                                    control={
                                      <Checkbox name="zakrytateritoria"  value={this.props.values.zakrytateritoria} onClick={(event)=>{ this.props.setFieldValue("zakrytateritoria",Boolean(event.target.checked));}}/>
                                    }
                                    label="Закрита територія"
                                  />
                              </FormControl>
                              <FormControl>
                                <TextField variant="outlined"
                                      style={{marginBottom:"7px"}}
                                      select
                                      error={this.props.touched.klasbudivli && Boolean(this.props.errors.klasbudivli)}
                                      label="Клас будівлі"
                                      name="klasbudivli"
                                      id="klasbudivli"
                                      value={this.props.values.klasbudivli}
                                      margin={"dense"}
                                      onChange={(e)=>{this.props.handleChange(e);
                                      
                                      }}

                                      placeholder="Виберіть клас будівлі"
                                      >


                                      <MenuItem value={1}>економ</MenuItem>
                                      <MenuItem value={2}>стандарт</MenuItem>
                                      <MenuItem value={3}>комфорт</MenuItem>
                                      <MenuItem value={4}>еліт</MenuItem>
                                  </TextField>
                                </FormControl>

                                <FormControl>
                                  <FormControlLabel
                                        control={
                                          <Checkbox name="kadastrovyi_budivlia"  value={this.props.values.kadastrovyi_budivlia}  onClick={(event)=>{ this.props.setFieldValue("kadastrovyi_budivlia",Boolean(event.target.checked));}}/>
                                        }
                                        label="Кадастровий номер"
                                      />
                                 </FormControl>
                                 <FormControl>
                       
                                    <TextField variant="outlined"
                                        readOnly
                                        style={{marginBottom:"7px"}}
                                        error={this.props.touched.planuvannia_budynku && Boolean(this.props.errors.planuvannia_budynku)}
                                        label="Планування будинку"
                                        name="planuvannia_budynku"
                                        id="planuvannia_budynku"
                                        value={this.props.values.planuvannia_budynku}
                                        margin={"dense"}
                                        onChange={(e)=>{
                                          this.props.handleChange(e);
                                        }}

                                        placeholder="Виберіть планування"
                                        >

                                    </TextField>
                            
                                    </FormControl>
                                    <ImagesUploadDraggable display={true} setState={this.props.setState} imgcount={8} statename={"photobud"} caption={"Фото будівлі"}/>
                                    <ImagesUploadDraggable display={true} setState={this.props.setState} imgcount={7} statename={"photoplanuvannia"} caption={"Планування будівлі"}/>

                                   

                       </FormGroup>
                       </ExpansionPanel>
            );
           }

           else{
             return null;
           }
        }
   }