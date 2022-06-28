'use strict';

/*

This is a React code, in static folder there are plugins to use React in Django Templates

TZ Part 4.C

*/

const e = React.createElement;

class GetData extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            items: []
        };
        this.get_data = this.get_data.bind(this)
    }

    render() {
        return (
            <React.Fragment>
                { this.state.items.map((items) => (
                    <tr key={items.id}>
                        <th scope="row">{items.id_from_sheet}</th>
                        <td>{items.order_number}</td>
                        <td>${items.price_usd}</td>
                        <td>₽{items.price_rub}</td>
                        <td>{items.delivery_date}</td>
                    </tr>
                ))}
            </React.Fragment>
        );
    }

    componentDidMount() {
        this.get_data()
        this.interval = setInterval(this.get_data, 17000)
    }

    componentWillUnmount() {
        clearInterval(this.interval)
    }

    get_data() {
        let fetch_url = "http://127.0.0.1:8000/get_data_from_db_react/";
        fetch(fetch_url)
            .then(res => res.json())
            .then((result) => {
                console.log("Result", result['data'])
                this.setState({
                    items: result['data']
                });
            },
            (error) => {
                console.log("ERROR", error)
            }
        )
    }
}

const domContainer = document.querySelector('#index');
ReactDOM.render(<GetData />, domContainer);