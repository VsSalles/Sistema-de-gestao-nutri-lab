function input_taba(){
        var input_taba = document.getElementById('input_tabagismo');
        var select_taba = document.getElementById('tabagismo');

        if (select_taba.value == 'N'){
            input_taba.disabled = true;
        }else{
            input_taba.disabled = false;
        }

  }

function input_atividade(){
    var input_atv = document.getElementById('input_atv');
    var select_atv = document.getElementById('atividade');
    var dias_atv = document.getElementById('dias_atv');
    var horario_atv = document.getElementById('horario_atv');


    if (input_atv.value == 'N'){
        select_atv.disabled = true;
        dias_atv.disabled = true;
        horario_atv.disabled = true;

        }else{
        select_atv.disabled = false;
        dias_atv.disabled = false;
        horario_atv.disabled = false;
        }
}


function downloadPDF() {
  const data = document.querySelector('.pdff');
  var codigo = document.querySelector('#codigo');

  var opt = {
    margin: 1,
    filename: "Consulta-" + codigo + ".pdf",
    html2canvas: { scale: 2 },
    jsPDF: { unit: "in", format: "a2", orientation: "l" },
  };

  html2pdf().set(opt).from(data).save();

} 

function btn_consulta(){
  var botao = document.getElementById('btn-consulta')
        botao.click();
}