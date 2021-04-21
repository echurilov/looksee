import { useState, useEffect } from 'react';

let db = "http://localhost:5000"

async function getData(event) {
  let form = new FormData(event.target.form)
  let cleanForm = Array.from(form).filter(([_,v]) => v!=="")  
  let params = new URLSearchParams(cleanForm)
  await fetch(`${db}/show?${params}`)
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
      <table><tr><td></td></tr></table>
    </div>
  );
}

export default Table;
