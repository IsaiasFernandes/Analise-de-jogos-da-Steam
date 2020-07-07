import React, { useState, useEffect } from "react";
import { Chart } from "react-google-charts";

function App(props) {
  const [options, setOptions] = useState({
    title: "Gráfico do Jogo Steam",
  });

  const [data, setData] = useState([]);

  useEffect(() => {
    setData([
      ["Linguagens", "Quantidade"],
      ["Falaram Bem", props.dados[0]],
      ["Falaram Mal", props.dados[1]],
    ]);
  }, []);

  return (
    <div>
      <div style={{ display: "flex" }}>
        <Chart
          width={"800px"}
          height={"600px"}
          chartType="PieChart"
          data={data}
          options={options}
        />
      </div>
    </div>
  );
}

export default App;
