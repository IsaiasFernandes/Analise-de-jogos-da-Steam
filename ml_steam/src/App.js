import React, { Fragment, useState } from "react";
import "bootswatch/dist/flatly/bootstrap.min.css";
import { Chart } from "react-google-charts";
import Graficos from "./components/Graficos";

import api from "./services/api";

function App() {
  const [dados, setDados] = useState();
  const [name, setName] = useState("");

  async function handleRegister(e) {
    e.preventDefault();

    const data = { name };

    try {
      const response = await api.post("games", data);
      alert("Desculpe a demora");
      setDados(response.data);
      console.log(dados);
    } catch (err) {
      alert("Erro: não há análises deste produto ou produto não existe!!");
    }
    setName("");
  }
  return (
    <Fragment>
      <div class="jumbotron">
        <h1 class="display-3">Analise de Jogos Steam</h1>
      </div>
      <form onSubmit={handleRegister}>
        <div class="form-group justify-content-center col-7">
          <div class="form-group ">
            <label
              class="text-justify font-weight-bold pl-3"
              for="inputAddress2"
            >
              Escreva aqui o jogo que vai ser analisado!
            </label>
            <div class="col">
              <input
                type="text"
                class="form-control"
                id="inputAddress2"
                placeholder="Pesquise aqui"
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
              <button type="submit" class="mt-2 btn btn-primary btn-lg mb-2">
                Enviar
              </button>
            </div>
          </div>
        </div>
      </form>
      {dados && (
        <div class="p-2">
          <h1>{dados[3]} </h1> <Graficos dados={dados} />
        </div>
      )}
    </Fragment>
  );
}

export default App;
