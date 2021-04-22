import { useState } from 'react';
import _ from 'lodash';

let db = "http://localhost:5000"
let graph = "http://localhost:7777/graph"

function ISOdate(seconds) {
  return new Date(seconds*1000).toISOString()
}

async function getData(event) {
  let form = new FormData(event.target.form)
  let cleanForm = Array.from(form).filter(([_,v]) => v!=="")  
  let params = new URLSearchParams(cleanForm)
  let response = await fetch(`${db}/show?${params}`)
  return await response.json()
}

function graphURL(data) {
  let groupedData = _.groupBy(data, a => [a.chip, a.label])
  let series = Object.entries(groupedData).map(([k,v]) => {
    let query = v.map(a => `${ISOdate(a.received)},${a.value}`).join(';')
    return k+'='+query
  })
  return `${graph}?${series.join("&")}`
}

function Table() {
  let [data, setData] = useState([])

  async function updateData(event) { setData(await getData(event)) }

  return (
    <div className="Table">
      <form>
        <fieldset>
          <label>Chip<input name="chip" onChange={updateData} /></label>
          <label>Label<input name="label" onChange={updateData}/></label>
          <label>Start<input type="datetime-local" name="start" onChange={updateData}/></label>
          <label>End<input type="datetime-local" name="end" onChange={updateData}/></label>
        </fieldset>
      </form>
      <table><tbody><tr><td>
        <img alt="mr" src={graphURL(data)}/>
      </td></tr></tbody></table>
    </div>
  );
}

export default Table;
