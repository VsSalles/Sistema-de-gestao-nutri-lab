function exibe_refeicao(){
        const form_refeicao = document.getElementById('form-refeicao')
        const form_opcao = document.getElementById('form-opcao')

        form_refeicao.style.display = "block"
        form_opcao.style.display = "none"

    }

function exibe_opcao(){
        const form_refeicao = document.getElementById('form-refeicao')
        const form_opcao = document.getElementById('form-opcao')

        form_refeicao.style.display = "none"
        form_opcao.style.display = "block"

    }

function downloadPDF() {
        const data = document.querySelector('.fundo-alimentar');
        var opt = {
          margin: 1,
          filename: "PlanoAlimentar.pdf",
          html2canvas: { scale: 2 },
          jsPDF: { unit: "in", format: "letter", orientation: "portrait" },
        };
      
        html2pdf().set(opt).from(data).save();
      }

function gera_cor(qtd=1){
        var bg_color = []
        var border_color = []
        for(let i = 0; i < qtd; i++){
            let r = Math.random() * 255;
            let g = Math.random() * 255;
            let b = Math.random() * 255;
            bg_color.push(`rgba(${r}, ${g}, ${b}, ${0.2})`)
            border_color.push(`rgba(${r}, ${g}, ${b}, ${1})`)
        }
        
        return [bg_color, border_color];
      }

function renderiza_pacientes(url){

        var user_element = document.getElementById('user');
        var user = user_element.value;

        fetch(url + user, {
            method: 'get',
        }).then(function(result){
            return result.json()
        }).then(function(data){
            const ctx = document.getElementById('pacientes').getContext('2d');
            var cores_consultas = gera_cor(qtd=5)
            const myChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Métricas de pacientes',
                        data: data.data,
                        backgroundColor: cores_consultas[0],
                        borderColor: cores_consultas[1],
                        borderWidth: 1
                    }]
                },
                
            });
    
    
        })
    
    }

function renderiza_consultas(url){

        var user_element = document.getElementById('user');
        var user = user_element.value;

      fetch(url + user, {
          method: 'get',
      }).then(function(result){
          return result.json()
      }).then(function(data){
          
          const ctx = document.getElementById('consultas').getContext('2d');
          var cores_consultas = gera_cor(qtd=4)
          const myChart = new Chart(ctx, {
              type: 'bar',
              data: {
                  labels: data.labels,
                  datasets: [{
                      label: 'Quantidade de consultas por status',
                      data: data.data,
                      backgroundColor: cores_consultas[0],
                      borderColor: cores_consultas[1],
                      borderWidth: 1
                  }]
              },
              
          });
  
  
      })
    
  }

function renderiza_consultas_meses(url){

    var user_element = document.getElementById('user');
    var user = user_element.value;

    fetch(url + user, {
        method: 'get',
    }).then(function(result){
        return result.json()
    }).then(function(data){
        
        const ctx = document.getElementById('consultas_mes').getContext('2d');
        var cores_consultas = gera_cor(qtd=12)
        const myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Consultas dos ultimos 12 meses',
                    data: data.data,
                    backgroundColor: cores_consultas[0],
                    borderColor: cores_consultas[1],
                    borderWidth: 1
                }]
            },
            
        });


    })
  
}

function renderiza_pacientes_objetivo(url){

    var user_element = document.getElementById('user');      
    var user = user_element.value;

  fetch(url + user, {
      method: 'get',
  }).then(function(result){
      return result.json()
  }).then(function(data){
      
      const ctx = document.getElementById('pacientes_objetivos').getContext('2d');
      var cores_consultas = gera_cor(qtd=3)
      const myChart = new Chart(ctx, {
          type: 'bar',
          data: {
              labels: data.labels,
              datasets: [{
                  label: 'Objetivos dos pacientes',
                  data: data.data,
                  backgroundColor: cores_consultas[0],
                  borderColor: cores_consultas[1],
                  borderWidth: 1
              }]
          },
          
      });


  })

}

function renderiza_pacientes_atividade(url){

    var user_element = document.getElementById('user');
    var user = user_element.value;

  fetch(url + user, {
      method: 'get',
  }).then(function(result){
      return result.json()
  }).then(function(data){
      
      const ctx = document.getElementById('pacientes_atv').getContext('2d');
      var cores_consultas = gera_cor(qtd=5)
      const myChart = new Chart(ctx, {
          type: 'bar',
          data: {
              labels: data.labels,
              datasets: [{
                  label: 'Atividade Fisica dos pacientes',
                  data: data.data,
                  backgroundColor: cores_consultas[0],
                  borderColor: cores_consultas[1],
                  borderWidth: 1
              }]
          },
          
      });


  })

}

function renderiza_consultas_canceladas(url){
    
    var user_element = document.getElementById('user');
    var user = user_element.value;

  fetch(url + user, {
      method: 'get',
  }).then(function(result){
      return result.json()
  }).then(function(data){
      
      const ctx = document.getElementById('consultas_canc').getContext('2d');
      var cores_consultas = gera_cor(qtd=4)
      const myChart = new Chart(ctx, {
          type: 'bar',
          data: {
              labels: data.labels,
              datasets: [{
                  label: 'Principais Motivos de cancelamentos de consultas',
                  data: data.data,
                  backgroundColor: cores_consultas[0],
                  borderColor: cores_consultas[1],
                  borderWidth: 1
              }]
          },
          
      });


  })

}

function edita_dados_paciente(){
    var id = document.getElementById('paciente').value;
    var registro = document.getElementById('registro').value;
    var url = 'http://127.0.0.1:8000/dados_paciente/' + id + '?registro=' + registro
    var peso = document.getElementById('peso');   
    var altura = document.getElementById('altura');
    var gordura = document.getElementById('gordura');
    var musculo = document.getElementById('musculo');
    var hdl = document.getElementById('hdl');
    var ldl = document.getElementById('ldl');
    var ctotal = document.getElementById('ctotal');
    var triglicerídios = document.getElementById('triglicerídios');


  fetch(url, {
      method: 'get',
  }).then(function(result){
      return result.json()
  }).then(function(data){
    
    console.log(data)
    peso.value =  data['dado_paciente']['peso']
    altura.value = data['dado_paciente']['altura']
    gordura.value = data['dado_paciente']['gordura']
    musculo.value = data['dado_paciente']['musculo']
    hdl.value = data['dado_paciente']['hdl']
    ldl.value = data['dado_paciente']['ldl']
    ctotal.value = data['dado_paciente']['ctotal']
    triglicerídios.value = data['dado_paciente']['triglicerídios']

  })

}