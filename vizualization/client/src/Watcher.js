'use strict'

const { Chart, Geom, Axis, Tooltip, LineAdvance, Coord, Label, Legend, View, Guide, Shape } = window.BizCharts;

function postJson(url, json, handler) {
	const request = new XMLHttpRequest();
	request.open("POST", url, true);
	request.setRequestHeader("Content-Type", "application/json");
	request.setRequestHeader('Access-Control-Allow-Origin', '*');
	request.onreadystatechange = handler;
	request.send(JSON.stringify(json));
}

function CustomChart(data, cols, width, height) {
	const y_axis_data_key = Object.keys(cols)[0]; 
	const x_axis_data_key = Object.keys(cols)[1];
	console.log(data, y_axis_data_key, x_axis_data_key);
	return <Chart height={height} data={data} padding="auto" forceFit>
		<Axis name={y_axis_data_key} />
		<Axis name={x_axis_data_key} />
		<Tooltip crosshairs={{type:'line'}}/>
		<Geom type="area" position={`${x_axis_data_key}*${y_axis_data_key}`} color={'orange'} />
		<Geom type="line" position={`${x_axis_data_key}*${y_axis_data_key}`} size={2} color={'orange'} />
	</Chart>
}

class Watcher extends React.Component {
	constructor(props) {
		super(props);

		this.state = {
			'vizualization_server_address': 'http://10.1.13.136:8003',
			'data': undefined,
			'bar_width': '40%',
			'bar_element_padding': '1vw'
		};

		this.save = this.save.bind(this);
		this.load = this.load.bind(this);
	}

	getPage() {
		const json = {
			'name': 'template'
		};
		const vizualization_server_address = this.state['vizualization_server_address'];
		const setStateFunction = this.setState.bind(this);
		postJson(vizualization_server_address + '/get', json, function() {
			if (this.readyState == 4 && this.status == 200) {
				setStateFunction({data: JSON.parse(this.response)});
		}});
	}

	componentDidMount() {
		setInterval(this.getPage.bind(this), 1000);
	}

	getSaveData() {
		return this.state;
	}

	save() {
		const saveData = this.getSaveData();
		const saveDataText = JSON.stringify(saveData);
		const today = new Date();
		const currentDate = today.getFullYear().toString()
			+ '-' + (today.getMonth() + 1).toString()
			+ '-' + today.getDate().toString();
		const currentTime = today.getHours()
			+ ":" + today.getMinutes()
			+ ":" + today.getSeconds();
		downloadFile('visualisation_client-save'
			+ '-' + currentDate
			+ '-' + currentTime
			+ '.json', saveDataText);
	}

	setSaveData(data) {
		this.setState(data);
	}

	load() {
		uploadFile('json', jsonText => {
			const json = JSON.parse(jsonText);
			this.setSaveData(json);
		});
	}

	getSaveLoadButtons() {
		return <div className='saveLoadButtons'>
			<button className='saveButton' onClick={this.save}>save</button>
			<button className='loadButton' onClick={this.load}>load</button>
		</div>;
	}

	getWatcherElements() {
		const data = this.state.data;
		const bar_width = this.state.bar_width;
		const bar_element_padding = this.state.bar_element_padding;
		const bar_element_height = `min(2vw, calc(calc(100vh / ${data.length}) - calc(2 * ${bar_element_padding})))`;
		
		return (
			<div className="WatcherElements">
			{
				Object.entries(data).map(
					(e, i) => {
						const percents_completed = 100 * e[1].current / e[1].total;
						const current_average_speed = e[1].average_speed;
						return (
							<div className='WatcherElement' key={i} style={{
								'width': `100%`
							}}>
								<div className='BarElement' style={{
									'padding': bar_element_padding,
									'width': `calc(100% - calc(2 * ${bar_element_padding}))`,
									'height': bar_element_height
								}}>
									<div className='BarDescription' style={{
										'width': `calc(100% - ${bar_width})`,
										'fontSize': bar_element_height
									}}>
										<div className="name">{e[0]}</div>
										<div className="average_speed">{current_average_speed.toFixed(2)} it/s</div>
									</div>
									<div className="Bar" style={{
										'width': bar_width
									}}>
										<div className='BarMoving' style={{
											width: percents_completed + '%'
										}}></div>
										<div className="BarPercents" style={{
											'width': bar_width,
											'fontSize': bar_element_height
										}}>
											{e[1].current + '/' + e[1].total + '  (' + Math.floor(percents_completed) + '%)'}
										</div>
									</div>
								</div>
								<div className="ChartElement" style={{
									'width': '100%'
								}}>
									{CustomChart(e[1].chart_data, {
										average_speed: {min: 0, max: Math.max(...e[1].chart_data.map(e => e.average_speed))},
										elapsed: {range: [0, Math.max(...e[1].chart_data.map(e => e.elapsed))]}
									}, 600, 300)}
								</div>
							</div>
						);
					}
				)
			}
			</div>
		);
	}

	render() {
		const data = this.state.data;
		
		return (
			<div className="Watcher">
				{this.getSaveLoadButtons()}
				{data ? this.getWatcherElements() : null}
			</div>
		);
	}
}