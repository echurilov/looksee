let db = "http://localhost:5000"

async function getData(event) {
  let form = new FormData(event.target.form)
  let cleanForm = Array.from(form).filter(([_,v]) => v!=="")  
  let params = new URLSearchParams(cleanForm)
  let response = await fetch(`${db}/show?${params}`)
  console.table(await response.json())
}

function Table() {
  return (
    <div className="Table">
      <form>
        <fieldset>
          <label>Chip<input name="chip" onChange={getData} /></label>
          <label>Label<input name="label" onChange={getData}/></label>
          <label>Start<input type="datetime-local" name="start" onChange={getData}/></label>
          <label>End<input type="datetime-local" name="end" onChange={getData}/></label>
        </fieldset>
      </form>
      <table><tr><td>
        <img src="http://127.0.0.1:7777/graph?Vcore=1,2;2,4;4,8&temp1=1,6;2,8;4,10"/>
        </td></tr>
      </table>
    </div>
  );
}

export default Table;
