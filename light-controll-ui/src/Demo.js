import React, {Component} from 'react'
import Roundy from 'roundy';
import RoundyGroup from 'roundy';
import axios from 'axios';
import {makeStyles} from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import Grid from '@material-ui/core/Grid';

// const useStyles =

export class Demo extends Component {
    constructor(props) {
        super(props);
        this.state = {
            max: 100,
            min: 0,
            color: '#00ff00',
            step: 10,
            brightness: 30,
            color_temperature: 5100,
            radius: 100,
            device_id: "EC22"
        };
        const tmp = this;
        axios.get('http://localhost:8070/api/v1/get_state')
            .then(function (response) {
                console.log(response);
                if (response.data) {
                    tmp.setState({brightness: response.data[tmp.state.device_id].settings.light_level_value});
                    tmp.setState({color_temperature: response.data[tmp.state.device_id].settings.color_temperature_value});
                }
            })
            .catch(function (error) {
                console.log(error);
            });
    }

    updateState() {
        axios.post('http://localhost:8070/api/v1/update_light', {
            device_id: this.state.device_id,
            settings: {
                light_level_value: this.state.brightness,
                color_temperature_value: this.state.color_temperature
            }
        })
            .then(function (response) {
                console.log(response);
            })
            .catch(function (error) {
                console.log(error);
            });
    }

    setLight(type) {
        axios.post('http://localhost:8070/api/v1/set_light', {
            device_id: this.state.device_id,
            settings: {
                light_level_value: this.state.brightness,
                color_temperature_value: this.state.color_temperature
            },
            type: type,
            user: "elizaveta"
        })
            .then(function (response) {
                console.log(response);
            })
            .catch(function (error) {
                console.log(error);
            });
    }

    update_brightness(val) {
        console.log("updating brightnesss to " + val);
        this.updateState()
    }

    update_color_temperature(val) {
        console.log("updating color temperature to " + val);
        this.updateState()
    }

    save_brightness(val) {
        console.log("saving brightnesss to " + val);
        this.setLight("brightness")

    }

    save_color_temperature(val) {
        console.log("saving color temperature to " + val);
        this.setLight("color")
    }

    render() {
        const classes = makeStyles(theme => ({
            root: {
                flexGrow: 1,
            },
            paper: {
                padding: theme.spacing(2),
                textAlign: 'center',
                color: theme.palette.text.secondary,
            },
        }));
        const {max, min, step, radius, color} = this.state;
        return (
            <div className={classes.root}>
                <Grid container spacing={3}>
                    <Grid item xs={12}>
                        <Paper className={classes.paper}>
                            <h1>Light Control Panel</h1>
                        </Paper>
                    </Grid>
                    <Grid item xs={6}>
                        <Paper className={classes.paper}>
                            <Roundy style={{margin: "20px"}}
                                allowClick
                                value={this.state.brightness}
                                radius={parseInt(radius)}
                                min={0}
                                max={100}
                                color={color}
                                stepSize={5}
                                arcSize={300}
                                sliced={false}
                                onChange={brightness => {
                                    this.setState({brightness: brightness});
                                    this.update_brightness(brightness)
                                }}
                                onAfterChange={(color_temperature, props) => {
                                    this.setState({brightness: props.value});
                                    this.save_brightness(props.value)
                                }}
                            />
                        </Paper>
                    </Grid>
                    <Grid item xs={6}>
                        <Paper className={classes.paper}>
                            <Roundy style={{margin: "20px"}}
                                allowClick
                                value={this.state.color_temperature}
                                radius={parseInt(radius)}
                                min={2700}
                                max={6500}
                                color={"#FF9C9B"}
                                stepSize={50}
                                arcSize={300}
                                sliced={false}
                                onChange={color_temperature => {
                                    this.setState({color_temperature: color_temperature});
                                    this.update_color_temperature(color_temperature)
                                }}
                                onAfterChange={(color_temperature, props) => {
                                    this.setState({color_temperature: props.value});
                                    this.save_color_temperature(props.value)
                                }}
                            />
                        </Paper>
                    </Grid>
                    <Grid item xs={6}>
                        <Paper className={classes.paper}>Brightness: {this.state.brightness}</Paper>
                    </Grid>

                    <Grid item xs={6}>
                        <Paper className={classes.paper}>Color temperature: {this.state.color_temperature}<br/></Paper>
                    </Grid>
                </Grid>
            </div>
        )
    }
}