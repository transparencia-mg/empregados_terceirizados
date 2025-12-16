/* Estilos customizados para o Dashboard de Terceirizados */

/* Animações */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.fade-in {
    animation: fadeIn 0.5s ease-out;
}

/* Estilos para tooltips melhorados */
.tooltip-custom {
    position: relative;
    display: inline-block;
    cursor: help;
}

.tooltip-custom .tooltip-text {
    visibility: hidden;
    width: 250px;
    background-color: var(--primary-dark);
    color: white;
    text-align: left;
    border-radius: 6px;
    padding: 10px;
    position: absolute;
    z-index: 1000;
    bottom: 125%;
    left: 50%;
    transform: translateX(-50%);
    opacity: 0;
    transition: opacity 0.3s;
    font-size: 12px;
    font-weight: normal;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    line-height: 1.4;
}

.tooltip-custom .tooltip-text::after {
    content: "";
    position: absolute;
    top: 100%;
    left: 50%;
    margin-left: -5px;
    border-width: 5px;
    border-style: solid;
    border-color: var(--primary-dark) transparent transparent transparent;
}

.tooltip-custom:hover .tooltip-text {
    visibility: visible;
    opacity: 1;
}

/* Estilos para badges de status */
.badge-ativo {
    background-color: #d4edda;
    color: #155724;
    padding: 4px 8px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: 600;
}

.badge-inativo {
    background-color: #f8d7da;
    color: #721c24;
    padding: 4px 8px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: 600;
}

/* Estilos para cards de destaque */
.highlight-card {
    background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
    border: 2px solid var(--accent-green);
    box-shadow: 0 6px 20px rgba(76, 175, 80, 0.1);
    transition: all 0.3s ease;
}

.highlight-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 25px rgba(76, 175, 80, 0.15);
}

/* Estilos para tabelas */
.table-striped-custom tbody tr:nth-of-type(odd) {
    background-color: rgba(44, 85, 48, 0.03);
}

.table-hover-custom tbody tr:hover {
    background-color: rgba(44, 85, 48, 0.08);
    cursor: pointer;
}

/* Estilos responsivos extras */
@media (max-width: 576px) {
    .table-container {
        border-radius: 8px;
        overflow-x: auto;
    }
    
    .metric-card {
        padding: 15px 10px;
    }
    
    .metric-value {
        font-size: 18px;
    }
}

/* Estilos para modais */
.modal-custom .modal-content {
    border-radius: 12px;
    border: none;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.modal-custom .modal-header {
    border-radius: 12px 12px 0 0;
    padding: 20px;
}

.modal-custom .modal-body {
    padding: 25px;
    max-height: 70vh;
    overflow-y: auto;
}

/* Estilos para botões */
.btn-success-custom {
    background: linear-gradient(135deg, var(--accent-green), #66bb6a);
    border: none;
    color: white;
    padding: 10px 20px;
    border-radius: 8px;
    font-weight: 600;
    transition: all 0.3s ease;
}

.btn-success-custom:hover {
    background: linear-gradient(135deg, #66bb6a, var(--accent-green));
    transform: translateY(-2px);
    box-shadow: 0 6px 15px rgba(76, 175, 80, 0.3);
    color: white;
}

/* Estilos para formulários */
.form-control-custom {
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    padding: 12px 15px;
    transition: all 0.3s ease;
}

.form-control-custom:focus {
    border-color: var(--accent-green);
    box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
}

/* Estilos para alertas */
.alert-custom {
    border-radius: 8px;
    border: none;
    padding: 15px 20px;
    margin-bottom: 20px;
}

.alert-success-custom {
    background-color: #d4edda;
    color: #155724;
    border-left: 4px solid var(--accent-green);
}

.alert-info-custom {
    background-color: #d1ecf1;
    color: #0c5460;
    border-left: 4px solid #17a2b8;
}

.alert-warning-custom {
    background-color: #fff3cd;
    color: #856404;
    border-left: 4px solid #ffc107;
}

.alert-danger-custom {
    background-color: #f8d7da;
    color: #721c24;
    border-left: 4px solid #dc3545;
}
