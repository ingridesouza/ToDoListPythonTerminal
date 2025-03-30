const BASE_URL = 'http://127.0.0.1:5000'; 
    const TAREFAS_POR_PAGINA = 5;

    // Gerenciamento de Categorias
    let categorias = JSON.parse(localStorage.getItem('categorias')) || ['Trabalho', 'Pessoal', 'Estudos'];
    let todasTarefas = []; 

    function exibirTarefas(tarefas, containerId, opcoes = {}) {
      const container = document.getElementById(containerId);
      container.innerHTML = '';
      
      if (!tarefas || tarefas.length === 0) {
        container.innerHTML = `
          <div class="alert">
            <i class="fas fa-info-circle"></i> Nenhuma tarefa encontrada.
          </div>
        `;
        return;
      }
      
      if (opcoes.modoSelecao) {
        const select = document.createElement('select');
        select.id = opcoes.selectId;
        select.className = 'select-tarefas';
        select.style.width = '100%';
        select.style.padding = '0.75rem';
        select.style.borderRadius = '6px';
        select.style.border = '1px solid var(--border-color)';
        select.style.marginBottom = '1rem';

        const optionPadrao = document.createElement('option');
        optionPadrao.value = '';
        optionPadrao.textContent = opcoes.placeholder || 'Selecione uma tarefa';
        select.appendChild(optionPadrao);
        

        tarefas.forEach(t => {
          const option = document.createElement('option');
          option.value = t.nome_tarefa;
          option.textContent = `${t.nome_tarefa} (${t.prioridade}) - ${t.status_tarefa ? 'Concluída' : 'Pendente'}`;
          select.appendChild(option);
        });
        
        container.appendChild(select);
        
        if (tarefas.length > TAREFAS_POR_PAGINA && opcoes.comBusca) {
          const buscaContainer = document.createElement('div');
          buscaContainer.style.marginBottom = '1rem';
          buscaContainer.innerHTML = `
            <input type="text" id="busca-${opcoes.selectId}" class="busca-tarefa" 
                   placeholder="Buscar tarefa..." style="width: 100%; padding: 0.5rem;">
          `;
          container.insertBefore(buscaContainer, select);
          

          document.getElementById(`busca-${opcoes.selectId}`).addEventListener('input', (e) => {
            const termo = e.target.value.toLowerCase();
            Array.from(select.options).forEach(option => {
              const deveMostrar = option.value === '' || option.textContent.toLowerCase().includes(termo);
              option.style.display = deveMostrar ? 'block' : 'none';
            });
          });
        }
        
        return;
      }

      const tarefaList = document.createElement('div');
      tarefaList.classList.add('tarefa-list');
      
      tarefas.forEach(t => {
        const divTarefa = document.createElement('div');
        divTarefa.classList.add('tarefa', 'fade-in');
        if (t.status_tarefa) {
          divTarefa.classList.add('tarefa-concluida');
        }
        
        let prioridadeClass = '';
        if (t.prioridade === 'Alta') prioridadeClass = 'prioridade-alta';
        else if (t.prioridade === 'Média') prioridadeClass = 'prioridade-media';
        else prioridadeClass = 'prioridade-baixa';
        
        divTarefa.innerHTML = `
          <span class="tarefa-prioridade ${prioridadeClass}">${t.prioridade}</span>
          <p><strong>Nome:</strong> ${t.nome_tarefa}</p>
          <p><strong>Descrição:</strong> ${t.descricao}</p>
          <span class="tarefa-categoria"><i class="fas fa-tag"></i> ${t.categoria}</span>
          <div class="tarefa-status ${t.status_tarefa ? 'status-concluido' : 'status-pendente'}">
            <i class="fas ${t.status_tarefa ? 'fa-check-circle' : 'fa-hourglass-half'}"></i>
            ${t.status_tarefa ? 'Concluída' : 'Pendente'}
          </div>
        `;
        tarefaList.appendChild(divTarefa);
      });
      
      container.appendChild(tarefaList);
      container.style.display = 'block';
    }

    function showAlert(message, type, containerId) {
      const container = document.getElementById(containerId);
      container.innerHTML = `
        <div class="alert alert-${type}">
          <i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'}"></i>
          ${message}
        </div>
      `;
      container.style.display = 'block';
      
      if (type === 'success') {
        setTimeout(() => {
          container.style.display = 'none';
        }, 5000);
      }
    }

    function atualizarCategorias() {
      const selectTarefa = document.getElementById('categoriaTarefa');
      selectTarefa.innerHTML = '<option value="">Selecione uma categoria</option>';
      
      const selectFiltro = document.getElementById('categoriaFiltro');
      selectFiltro.innerHTML = '<option value="">Todas categorias</option>';
      
      const listaCategorias = document.getElementById('listaCategorias');
      listaCategorias.innerHTML = '';
      
      if (categorias.length === 0) {
        listaCategorias.innerHTML = '<p class="alert"><i class="fas fa-info-circle"></i> Nenhuma categoria cadastrada.</p>';
      } else {
        const ul = document.createElement('ul');
        ul.style.listStyle = 'none';
        ul.style.padding = '0';
        
        categorias.forEach((cat, index) => {
          const optionTarefa = document.createElement('option');
          optionTarefa.value = cat;
          optionTarefa.textContent = cat;
          selectTarefa.appendChild(optionTarefa);
          
          const optionFiltro = document.createElement('option');
          optionFiltro.value = cat;
          optionFiltro.textContent = cat;
          selectFiltro.appendChild(optionFiltro);
          
          const li = document.createElement('li');
          li.style.display = 'flex';
          li.style.justifyContent = 'space-between';
          li.style.alignItems = 'center';
          li.style.padding = '0.5rem';
          li.style.borderBottom = '1px solid var(--border-color)';
          
          li.innerHTML = `
            <span>${cat}</span>
            <button class="btn btn-icon btn-danger remover-categoria" data-index="${index}">
              <i class="fas fa-trash"></i>
            </button>
          `;
          ul.appendChild(li);
        });
        
        listaCategorias.appendChild(ul);
      }
      
      localStorage.setItem('categorias', JSON.stringify(categorias));
    }

    async function carregarTarefasParaSelecao() {
      try {
        const response = await fetch(`${BASE_URL}/tarefas`);
        todasTarefas = await response.json();
        
        if (document.getElementById('selectConcluirTarefa')) {
          exibirTarefas(todasTarefas, 'selectConcluirTarefa', {
            modoSelecao: true,
            selectId: 'nomeConcluir',
            placeholder: 'Selecione a tarefa para concluir',
            comBusca: todasTarefas.length > TAREFAS_POR_PAGINA
          });
        }
        
        if (document.getElementById('selectRemoverTarefa')) {
          exibirTarefas(todasTarefas, 'selectRemoverTarefa', {
            modoSelecao: true,
            selectId: 'nomeRemover',
            placeholder: 'Selecione a tarefa para remover',
            comBusca: todasTarefas.length > TAREFAS_POR_PAGINA
          });
        }
      } catch (err) {
        console.error('Erro ao carregar tarefas para seleção:', err);
      }
    }

    // Navegação por abas
    document.querySelectorAll('.nav-tab').forEach(tab => {
      tab.addEventListener('click', () => {
        document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        
        tab.classList.add('active');
        const tabId = tab.getAttribute('data-tab');
        document.getElementById(tabId).classList.add('active');
        
        if (tabId === 'gerenciar') {
          carregarTarefasParaSelecao();
        }
      });
    });

    // 1. LISTAR TODAS AS TAREFAS
    document.getElementById('btnListarTarefas').addEventListener('click', (e) => {
      e.preventDefault();
      const container = document.getElementById('listaTarefas');
      container.innerHTML = '<p><i class="fas fa-spinner fa-spin"></i> Carregando tarefas...</p>';
      
      fetch(`${BASE_URL}/tarefas`)
        .then(res => res.json())
        .then(data => {
          exibirTarefas(data, 'listaTarefas');
          todasTarefas = data;
        })
        .catch(err => {
          container.innerHTML = `
            <div class="alert alert-error">
              <i class="fas fa-exclamation-triangle"></i> Erro ao carregar tarefas. Tente novamente.
            </div>
          `;
          console.error(err);
        });
    });

    // 2. ADICIONAR NOVA CATEGORIA
    document.getElementById('btnAddCategoria').addEventListener('click', (e) => {
      e.preventDefault();
      const input = document.getElementById('novaCategoria');
      const categoria = input.value.trim();
      
      if (!categoria) {
        showAlert('Digite um nome para a categoria', 'error', 'listaCategorias');
        return;
      }
      
      if (categorias.includes(categoria)) {
        showAlert('Esta categoria já existe', 'error', 'listaCategorias');
        return;
      }
      
      categorias.push(categoria);
      input.value = '';
      atualizarCategorias();
      showAlert(`Categoria "${categoria}" adicionada!`, 'success', 'listaCategorias');
    });

    // 3. REMOVER CATEGORIA
    document.getElementById('listaCategorias').addEventListener('click', (e) => {
      if (e.target.closest('.remover-categoria')) {
        const index = e.target.closest('.remover-categoria').getAttribute('data-index');
        const categoriaRemovida = categorias[index];
        categorias.splice(index, 1);
        atualizarCategorias();
        showAlert(`Categoria "${categoriaRemovida}" removida!`, 'success', 'listaCategorias');
      }
    });

    // 4. CRIAR UMA NOVA TAREFA
    document.getElementById('formCriarTarefa').addEventListener('submit', function (e) {
      e.preventDefault();
      
      const nome = document.getElementById('nomeTarefa').value;
      const descricao = document.getElementById('descricaoTarefa').value;
      const prioridade = document.getElementById('prioridadeTarefa').value;
      const categoria = document.getElementById('categoriaTarefa').value;
      
      if (!categoria) {
        showAlert('Selecione uma categoria', 'error', 'resCriarTarefa');
        return;
      }
      
      const container = document.getElementById('resCriarTarefa');
      container.innerHTML = '<p><i class="fas fa-spinner fa-spin"></i> Criando tarefa...</p>';
      container.style.display = 'block';
      
      fetch(`${BASE_URL}/tarefas`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ 
          nome, 
          descricao, 
          prioridade, 
          categoria 
        })
      })
      .then(res => res.json())
      .then(data => {
        if (data.erro) {
          showAlert(data.erro, 'error', 'resCriarTarefa');
        } else {
          showAlert(data.mensagem || 'Tarefa criada com sucesso!', 'success', 'resCriarTarefa');
          this.reset();
          todasTarefas.push({ nome_tarefa: nome, descricao, prioridade, categoria, status_tarefa: false });
          
          if (document.getElementById('listar').classList.contains('active')) {
            document.getElementById('btnListarTarefas').click();
          }
          
          if (document.getElementById('gerenciar').classList.contains('active')) {
            carregarTarefasParaSelecao();
          }
        }
      })
      .catch(err => {
        showAlert('Erro ao criar tarefa. Verifique sua conexão.', 'error', 'resCriarTarefa');
        console.error(err);
      });
    });
      
    // 5. REMOVER TAREFA
    document.getElementById('formRemoverTarefa').addEventListener('submit', function (e) {
      e.preventDefault();
      const nomeRemover = document.getElementById('nomeRemover').value;
      
      if (!nomeRemover) {
        showAlert('Selecione uma tarefa para remover', 'error', 'resGerenciarTarefas');
        return;
      }
      
      const container = document.getElementById('resGerenciarTarefas');
      container.innerHTML = '<p><i class="fas fa-spinner fa-spin"></i> Removendo tarefa...</p>';
      container.style.display = 'block';
      
      fetch(`${BASE_URL}/tarefas/${encodeURIComponent(nomeRemover)}`, {
        method: 'DELETE'
      })
      .then(res => res.json())
      .then(data => {
        if (data.erro) {
          showAlert(data.erro, 'error', 'resGerenciarTarefas');
        } else {
          showAlert(data.mensagem || 'Tarefa removida com sucesso!', 'success', 'resGerenciarTarefas');
          
          todasTarefas = todasTarefas.filter(t => t.nome_tarefa !== nomeRemover);
          
          carregarTarefasParaSelecao();
          
          if (document.getElementById('listar').classList.contains('active')) {
            document.getElementById('btnListarTarefas').click();
          }
        }
      })
      .catch(err => {
        showAlert('Erro ao remover tarefa. Verifique sua conexão.', 'error', 'resGerenciarTarefas');
        console.error(err);
      });
    });

    // 6. MARCAR CONCLUÍDA (AGORA COM SELECT)
    document.getElementById('formConcluirTarefa').addEventListener('submit', function (e) {
      e.preventDefault();
      const nomeConcluir = document.getElementById('nomeConcluir').value;
      
      if (!nomeConcluir) {
        showAlert('Selecione uma tarefa para concluir', 'error', 'resGerenciarTarefas');
        return;
      }
      
      const container = document.getElementById('resGerenciarTarefas');
      container.innerHTML = '<p><i class="fas fa-spinner fa-spin"></i> Atualizando tarefa...</p>';
      container.style.display = 'block';
      
      fetch(`${BASE_URL}/tarefas/${encodeURIComponent(nomeConcluir)}/concluir`, {
        method: 'PUT'
      })
      .then(res => res.json())
      .then(data => {
        if (data.erro) {
          showAlert(data.erro, 'error', 'resGerenciarTarefas');
        } else {
          showAlert(data.mensagem || 'Tarefa marcada como concluída!', 'success', 'resGerenciarTarefas');
          
          const tarefa = todasTarefas.find(t => t.nome_tarefa === nomeConcluir);
          if (tarefa) {
            tarefa.status_tarefa = true;
          }
          
          carregarTarefasParaSelecao();
          
          if (document.getElementById('listar').classList.contains('active')) {
            document.getElementById('btnListarTarefas').click();
          }
        }
      })
      .catch(err => {
        showAlert('Erro ao concluir tarefa. Verifique sua conexão.', 'error', 'resGerenciarTarefas');
        console.error(err);
      });
    });

    // 7. FILTRAR TAREFAS
    document.getElementById('formFiltrarPrioridade').addEventListener('submit', function (e) {
      e.preventDefault();
      const prioridadeFiltro = document.getElementById('prioridadeFiltro').value;
      const categoriaFiltro = document.getElementById('categoriaFiltro').value;
      
      const container = document.getElementById('resFiltrarTarefas');
      container.innerHTML = '<p><i class="fas fa-spinner fa-spin"></i> Filtrando tarefas...</p>';
      container.style.display = 'block';
      
      let url = `${BASE_URL}/tarefas`;
      if (prioridadeFiltro && categoriaFiltro) {
        url = `${BASE_URL}/tarefas/filtro?prioridade=${encodeURIComponent(prioridadeFiltro)}&categoria=${encodeURIComponent(categoriaFiltro)}`;
      } else if (prioridadeFiltro) {
        url = `${BASE_URL}/tarefas/prioridade/${encodeURIComponent(prioridadeFiltro)}`;
      } else if (categoriaFiltro) {
        url = `${BASE_URL}/tarefas/categoria/${encodeURIComponent(categoriaFiltro)}`;
      }
      
      fetch(url)
        .then(res => res.json())
        .then(data => exibirTarefas(data, 'resFiltrarTarefas'))
        .catch(err => {
          container.innerHTML = `
            <div class="alert alert-error">
              <i class="fas fa-exclamation-triangle"></i> Erro ao filtrar tarefas. Tente novamente.
            </div>
          `;
          console.error(err);
        });
    });

    document.addEventListener('DOMContentLoaded', () => {
      atualizarCategorias();
      carregarTarefasParaSelecao();
    });