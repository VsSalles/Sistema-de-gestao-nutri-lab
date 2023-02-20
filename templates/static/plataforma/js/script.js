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
        console.log('fui chamada')
        const data = document.querySelector('.fundo-alimentar');
        var opt = {
          margin: 1,
          filename: "PlanoAlimentar.pdf",
          html2canvas: { scale: 2 },
          jsPDF: { unit: "in", format: "letter", orientation: "portrait" },
        };
      
        html2pdf().set(opt).from(data).save();
      }
