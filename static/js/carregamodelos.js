    function carregarModelos() {
        const marcaId = document.getElementById('marca').value;
        const modeloSelect = document.getElementById('modelo');

        // Limpa os modelos atuais
        modeloSelect.innerHTML = '<option value="">Todos</option>';

        if (marcaId) {
            fetch(`/get-modelos/${marcaId}/`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Erro ao carregar modelos: ' + response.status);
                    }
                    return response.json();
                })
                .then(data => {
                    data.forEach(modelo => {
                        const option = document.createElement('option');
                        option.value = modelo.id;
                        option.textContent = modelo.nome;
                        modeloSelect.appendChild(option);
                    });
                })
                .catch(err => {
                    console.error(err);
                });
        }
    }