"""Guia pratico dos principais recursos do Biopython.

Biopython e uma colecao de modulos Python para bioinformatica. Ele nao e uma
linguagem nova: continua sendo Python, mas oferece objetos e ferramentas para
sequencias, arquivos biologicos, alinhamentos, estruturas 3D e bancos de
dados.

Instalacao no terminal:

    py -m pip install biopython

Importante:
    O pacote instalado chama-se "biopython", mas os imports usam "Bio".
    Exemplo: from Bio.Seq import Seq

Documentacao oficial:
    https://biopython.org/docs/latest/

COMO ESTUDAR ESTE ARQUIVO
--------------------------
1. Instale o pacote com o comando acima.
2. Execute este arquivo para ver os exemplos locais:

    py explicacoes\\explicacao_biopython.py

3. Leia as funcoes que possuem comentarios com arquivos externos antes de
   tentar usa-las em seus proprios dados.

Este guia apresenta os recursos mais usados. Biopython e grande e possui
outros submodulos; a documentacao oficial continua sendo a referencia para
detalhes de cada versao.
"""


# ---------------------------------------------------------------------------
# 1. IDEIA GERAL
# ---------------------------------------------------------------------------
# Os objetos mais importantes sao:
#
# Seq       -> uma sequencia biologica, como DNA, RNA ou proteina.
# SeqRecord -> sequencia mais metadados: id, descricao, qualidade e features.
# SeqIO     -> le e grava SeqRecord em FASTA, GenBank, FASTQ e outros formatos.
# Align     -> cria e analisa alinhamentos de sequencias.
# AlignIO   -> le e grava arquivos de alinhamento.
# Entrez    -> acessa bancos do NCBI pela internet.
# PDB       -> le e analisa estruturas tridimensionais de proteinas.
# Phylo     -> trabalha com arvores filogeneticas.
# motifs    -> analisa motivos e padroes em sequencias.
# Restriction -> simula enzimas de restricao.
#
# O projeto e dividido em modulos para que voce importe somente o que precisa.
#
# Regra pratica:
# - Se voce tem uma sequencia pequena em uma variavel, comece com Seq.
# - Se a sequencia veio de um arquivo ou possui id/descricao, use SeqRecord.
# - Se precisa ler ou gravar muitos registros, use SeqIO.
# - Se precisa comparar sequencias, use Align.
# - Se precisa consultar o NCBI, use Entrez.


# ---------------------------------------------------------------------------
# 0. BIOLOGIA ESSENCIAL PARA ENTENDER OS EXEMPLOS
# ---------------------------------------------------------------------------
# DNA costuma ser escrito com A, T, C e G:
#     A (adenina) combina com T (timina)
#     C (citosina) combina com G (guanina)
#
# RNA usa U (uracila) no lugar de T. Uma sequencia de tres bases e um codon.
# Durante a traducao, cada codon pode representar um aminoacido ou STOP.
#
# Biopython realiza operacoes computacionais; ele nao decide se uma amostra
# esta biologicamente correta. A qualidade da entrada e a interpretacao dos
# resultados continuam sendo responsabilidade de quem faz a analise.


def exemplo_bases_e_codons():
    """Mostra indices, codons e uma verificacao simples de entrada."""
    from Bio.Seq import Seq

    dna = Seq("ATGGCCTAA")
    print("Bases numeradas a partir de zero:")
    for indice, base in enumerate(dna):
        print(indice, base)

    print("Codons de tres bases:", [dna[i : i + 3] for i in range(0, len(dna), 3)])
    print("Apenas DNA:", set(dna) <= set("ACGT"))
    print("Quantidade de A:", dna.count("A"))
    print("Percentual de GC:", 100 * (dna.count("G") + dna.count("C")) / len(dna))

    # A expressao [i:i+3] usa a mesma regra de fatias do Python:
    # o inicio entra e o fim nao entra.


def exemplo_seq():
    """Mostra operacoes comuns com DNA, RNA e proteina."""
    from Bio.Seq import Seq

    dna = Seq("ATGGCCTAA")
    print("DNA:", dna)
    print("Tipo:", type(dna).__name__)
    print("Tamanho:", len(dna))
    print("Primeiras tres bases:", dna[:3])
    print("Contagem de G:", dna.count("G"))

    # O complemento troca cada base pela sua complementar.
    print("Complemento:", dna.complement())
    print("Complemento reverso:", dna.reverse_complement())

    # Transcricao: DNA -> RNA. A timina vira uracila.
    rna = dna.transcribe()
    print("RNA:", rna)
    print("DNA recriado a partir do RNA:", rna.back_transcribe())

    # Traducao: RNA/DNA -> aminoacidos.
    # O asterisco representa um stop no codigo genetico.
    print("Proteina:", rna.translate())
    print("Proteina sem mostrar o stop final:", rna.translate(to_stop=True))

    # Uma sequencia pode ser convertida para str quando uma API comum espera
    # uma string normal.
    print("Como string:", str(dna))

    # Seq e imutavel, como uma string. Para trocar uma base, crie outra Seq:
    trocada = dna[:2] + "C" + dna[3:]
    print("Nova sequencia com uma troca:", trocada)

    # Operacoes biologicas exigem o tipo de sequencia adequado.
    proteina = Seq("MALW")
    print("Proteina:", proteina)
    # complement() e reverse_complement() nao fazem sentido para proteinas.


def exemplo_sequencia_invalida():
    """Explica a validacao opcional de alfabetos biologicos."""
    from Bio.Seq import Seq

    dna = Seq("ATGXYZ")
    print("Seq aceita:", dna)
    print(
        "Seq nao valida automaticamente todas as letras; "
        "valide sua entrada quando necessario."
    )

    def dna_valido(sequencia):
        """Retorna True se a sequencia contem apenas A, C, G e T."""
        texto = str(sequencia).upper()
        return bool(texto) and set(texto) <= set("ACGT")

    print("ATGC valido:", dna_valido("ATGC"))
    print("ATGXYZ valido:", dna_valido(dna))

    # Em dados reais, N pode representar uma base desconhecida. Decida
    # explicitamente se sua analise deve aceitar ou rejeitar esse simbolo.


# ---------------------------------------------------------------------------
# 2. SeqRecord: SEQUENCIA COM IDENTIFICACAO E ANOTACOES
# ---------------------------------------------------------------------------
def exemplo_seqrecord():
    from Bio.Seq import Seq
    from Bio.SeqRecord import SeqRecord

    registro = SeqRecord(
        Seq("ATGGCCTAA"),
        id="exemplo_001",
        name="gene_exemplo",
        description="Um gene usado para demonstracao",
    )

    print("Id:", registro.id)
    print("Nome:", registro.name)
    print("Descricao:", registro.description)
    print("Sequencia:", registro.seq)

    # annotations guarda informacoes gerais; features guarda regioes
    # biologicas, como genes, CDS e promotores.
    registro.annotations["organism"] = "Exemplo species"
    registro.annotations["molecule_type"] = "DNA"
    registro.letter_annotations["phred_quality"] = [40] * len(registro)
    print("Organismo:", registro.annotations["organism"])
    print("Tipo de molecula:", registro.annotations["molecule_type"])
    print("Qualidade da primeira base:", registro.letter_annotations["phred_quality"][0])
    print("Features:", registro.features)

    # O registro pode ser cortado como uma sequencia.
    parte = registro[0:6]
    print("Parte cortada:", parte.id, parte.seq)

    # Uma feature descreve uma regiao anotada. Location usa coordenadas
    # biologicas no formato do Biopython; o fim da regiao e exclusivo.
    from Bio.SeqFeature import FeatureLocation, SeqFeature

    gene = SeqFeature(
        FeatureLocation(0, 9),
        type="CDS",
        qualifiers={"gene": ["gene_exemplo"], "product": ["proteina exemplo"]},
    )
    registro.features.append(gene)
    print("Feature criada:", registro.features[0].type)
    print("Regiao da feature:", registro.features[0].location)
    print("Qualifiers:", registro.features[0].qualifiers)


# ---------------------------------------------------------------------------
# 3. SeqIO: ARQUIVOS FASTA, GENBANK E FASTQ
# ---------------------------------------------------------------------------
def exemplo_seqio():
    from io import StringIO

    from Bio import SeqIO
    from Bio.Seq import Seq
    from Bio.SeqRecord import SeqRecord

    registros = [
        SeqRecord(Seq("ATGC"), id="seq1", description="Primeira sequencia"),
        SeqRecord(Seq("GGCA"), id="seq2", description="Segunda sequencia"),
    ]

    # StringIO permite testar sem criar arquivo no disco.
    fasta_em_memoria = StringIO()
    SeqIO.write(registros, fasta_em_memoria, "fasta")
    conteudo = fasta_em_memoria.getvalue()
    print("FASTA produzido:")
    print(conteudo)

    fasta_em_memoria.seek(0)
    lidos = list(SeqIO.parse(fasta_em_memoria, "fasta"))
    for registro in lidos:
        print(registro.id, len(registro.seq), registro.description)

    # parse() serve para zero, um ou muitos registros.
    # read() exige exatamente um registro e gera erro se houver mais.
    #
    # Arquivo FASTA:
    # for registro in SeqIO.parse("sequencias.fasta", "fasta"):
    #     print(registro.id, registro.seq)
    #
    # Gravar:
    # SeqIO.write(lidos, "copia.fasta", "fasta")
    #
    # Formatos frequentes:
    # "fasta", "fastq", "genbank", "embl", "tab", "phd", "sff".

    # FASTA e simples: uma linha com ">" e identificacao, seguida da
    # sequencia. Ele normalmente nao guarda organismo, features ou qualidade.
    # GenBank e mais rico em anotacoes. FASTQ guarda qualidade por base.


def exemplo_filtrar_sequencias():
    """Filtra registros e calcula uma estatistica simples."""
    from Bio import SeqIO
    from Bio.Seq import Seq
    from Bio.SeqRecord import SeqRecord

    registros = [
        SeqRecord(Seq("ATGC"), id="curta"),
        SeqRecord(Seq("ATGCGCGC"), id="longa"),
        SeqRecord(Seq("NNNN"), id="desconhecida"),
    ]

    aproveitadas = [
        registro
        for registro in registros
        if len(registro) >= 5 and "N" not in registro.seq
    ]
    print("Registros aproveitados:", [registro.id for registro in aproveitadas])

    # O padrao e sempre: parse -> filtrar -> transformar -> write.
    # SeqIO.write(aproveitadas, "filtradas.fasta", "fasta")


def exemplo_indice_seqio():
    """Mostra como buscar registros grandes sem carregar todos na memoria."""
    from Bio import SeqIO

    # index() e index_db() permitem acesso por id em arquivos de sequencia.
    # O arquivo precisa existir para executar este exemplo.
    #
    # registros = SeqIO.index("sequencias.fasta", "fasta")
    # print(registros["id_da_sequencia"].seq)
    # registros.close()
    #
    # index_db() cria um indice persistente SQLite:
    # registros = SeqIO.index_db("indice.sqlite", "sequencias.fasta", "fasta")
    pass


# ---------------------------------------------------------------------------
# 4. QUALIDADE DE SEQUENCIAMENTO: FASTQ
# ---------------------------------------------------------------------------
def exemplo_fastq():
    from Bio import SeqIO

    # FASTQ armazena sequencia e qualidade de cada base.
    #
    # for registro in SeqIO.parse("leituras.fastq", "fastq"):
    #     qualidade = registro.letter_annotations["phred_quality"]
    #     print(registro.id, registro.seq, qualidade)
    #
    # Os valores de qualidade sao interpretados pelo formato informado.
    # Nao troque "fastq" por "fasta": FASTA nao possui qualidades.

    # Uma forma comum de filtrar leituras:
    #
    # boas = []
    # for registro in SeqIO.parse("leituras.fastq", "fastq"):
    #     qualidades = registro.letter_annotations["phred_quality"]
    #     media = sum(qualidades) / len(qualidades)
    #     if media >= 30:
    #         boas.append(registro)
    # SeqIO.write(boas, "leituras_boas.fastq", "fastq")
    #
    # PHRED maior geralmente significa menor probabilidade de erro, mas o
    # significado exato depende da codificacao do formato FASTQ.
    pass


# ---------------------------------------------------------------------------
# 5. FORMATOS DE ANOTACAO: GENBANK E EMBL
# ---------------------------------------------------------------------------
def exemplo_genbank():
    from Bio import SeqIO

    # GenBank possui sequencia, organismo, referencias e features.
    #
    # registro = SeqIO.read("arquivo.gb", "genbank")
    # print(registro.annotations)
    # for feature in registro.features:
    #     print(feature.type, feature.location, feature.qualifiers)
    #
    # Para preservar anotacoes ao gravar, use SeqRecord e o formato correto:
    # SeqIO.write(registro, "saida.gb", "genbank")

    # Localizacoes podem ser:
    # 5..20       regiao continua
    # complement(5..20) fita reversa
    # join(5..10,30..40) partes combinadas
    #
    # Ao extrair uma feature:
    # sequencia_da_feature = feature.extract(registro.seq)
    pass


# ---------------------------------------------------------------------------
# 6. ALINHAMENTO DE SEQUENCIAS
# ---------------------------------------------------------------------------
def exemplo_alinhamento():
    from Bio import Align

    alinhador = Align.PairwiseAligner()
    alinhador.match_score = 2
    alinhador.mismatch_score = -1
    alinhador.open_gap_score = -2
    alinhador.extend_gap_score = -0.5

    alinhamentos = alinhador.align("ACCGT", "ACG")
    print("Quantidade de melhores alinhamentos:", len(alinhamentos))
    print(alinhamentos[0])
    print("Pontuacao:", alinhamentos[0].score)

    # Para multiplas sequencias, use MultipleSeqAlignment e AlignIO.
    # from Bio import AlignIO
    # alinhamento = AlignIO.read("alinhamento.fasta", "fasta")
    # print(alinhamento)
    #
    # Em arquivos de alinhamento, todas as sequencias normalmente precisam
    # ter o mesmo tamanho, usando "-" para gaps.

    # Match, mismatch e gap sao escolhas do modelo. Alterar as pontuacoes
    # pode mudar o melhor alinhamento; nao existe uma pontuacao universal.
    # O resultado do alinhamento e um objeto, nao apenas uma string.


def exemplo_identidade():
    """Calcula identidade de duas sequencias de mesmo tamanho."""
    from Bio.Seq import Seq

    a = Seq("ATGCCA")
    b = Seq("ATGACA")
    iguais = sum(base_a == base_b for base_a, base_b in zip(a, b))
    identidade = 100 * iguais / len(a)
    print("Identidade sem gaps:", identidade, "%")

    # Para sequencias de tamanhos diferentes, alinhe primeiro. Comparar
    # posicao por posicao sem alinhamento pode produzir uma conclusao errada.


# ---------------------------------------------------------------------------
# 7. MOTIFS E ENZIMAS DE RESTRICAO
# ---------------------------------------------------------------------------
def exemplo_motifs():
    from Bio import motifs
    from Bio.Seq import Seq

    # Um motivo e um padrao recorrente em sequencias.
    instancias = [Seq("ATGC"), Seq("ATGA"), Seq("ATGT")]
    motivo = motifs.create(instancias)
    print("Consenso do motivo:", motivo.consensus)
    print("Anticonsenso:", motivo.anticonsensus)
    print("Contagem de bases:", motivo.counts)

    # PWM (Position Weight Matrix) representa a frequencia de cada letra por
    # posicao. Ela pode ser usada para pontuar uma nova sequencia:
    # pwm = motivo.counts.normalize(pseudocounts=0.5).log_odds()
    # print(pwm.calculate(Seq("ATGC")))


def exemplo_restriction():
    from Bio.Restriction import EcoRI
    from Bio.Seq import Seq

    dna = Seq("AAAAGAATTCAAAA")
    print("Cortes da EcoRI:", EcoRI.search(dna))
    print("Fragmentos:", EcoRI.catalyze(dna))
    print("Sitio de reconhecimento:", EcoRI.site)
    print("Comprimento do sitio:", EcoRI.size)

    # search() retorna posicoes de corte na sequencia, usando coordenadas
    # baseadas em 1. Isso e diferente do indice inicial baseado em 0 do
    # Python. Sempre confira a convencao antes de combinar resultados.


# ---------------------------------------------------------------------------
# 8. Entrez: CONSULTAR O NCBI
# ---------------------------------------------------------------------------
def exemplo_entrez():
    from Bio import Entrez, SeqIO

    # NCBI pede um email para identificar o usuario. Use o seu email real.
    # Entrez.email = "seu.email@example.com"
    #
    # with Entrez.esearch(db="nucleotide", term="Homo sapiens[organism]") as
    #     resposta:
    #     resultado = Entrez.read(resposta)
    #
    # ids = resultado["IdList"]
    # with Entrez.efetch(
    #     db="nucleotide", id=ids[:1], rettype="fasta", retmode="text"
    # ) as resposta:
    #     print(resposta.read())
    #
    # Para GenBank, use:
    # registro = SeqIO.read(resposta, "genbank")
    #
    # Respeite limites de requisicoes, use cache quando possivel e trate
    # erros de rede. Entrez acessa a internet e pode demorar.
    #
    # Fluxo recomendado:
    # 1. esearch encontra IDs.
    # 2. esummary traz um resumo dos resultados.
    # 3. efetch baixa o registro completo.
    # 4. SeqIO interpreta o texto biologico.
    #
    # Para varias requisicoes, evite baixar o mesmo registro repetidamente.
    # Tambem nao coloque sua chave de API ou senha dentro deste arquivo.
    pass


# ---------------------------------------------------------------------------
# 9. ESTRUTURAS 3D COM Bio.PDB
# ---------------------------------------------------------------------------
def exemplo_pdb():
    from Bio.PDB import PDBParser

    # O arquivo PDB precisa existir para executar:
    # parser = PDBParser(QUIET=True)
    # estrutura = parser.get_structure("proteina", "estrutura.pdb")
    # for modelo in estrutura:
    #     for cadeia in modelo:
    #         for residuo in cadeia:
    #             for atomo in residuo:
    #                 print(atomo.name, atomo.coord)
    #
    # A hierarquia usual e:
    # Structure -> Model -> Chain -> Residue -> Atom.
    #
    # Para arquivos mmCIF, use MMCIFParser:
    # from Bio.PDB import MMCIFParser
    # parser = MMCIFParser(QUIET=True)
    # estrutura = parser.get_structure("proteina", "estrutura.cif")
    #
    # As coordenadas de um atomo ficam em atomo.coord, normalmente como tres
    # valores x, y e z. PDB trabalha com dados espaciais, nao com sequencias
    # simples; por isso a navegacao passa por modelos e cadeias.
    pass


# ---------------------------------------------------------------------------
# 10. ARVORES FILOGENETICAS COM Bio.Phylo
# ---------------------------------------------------------------------------
def exemplo_phylo():
    from Bio import Phylo

    # arvore = Phylo.read("arvore.nwk", "newick")
    # print(arvore)
    # Phylo.draw_ascii(arvore)
    # Phylo.write(arvore, "copia.nwk", "newick")
    #
    # O formato Newick representa ramificacoes com parenteses. Outros
    # formatos suportados podem conter mais informacoes de anotacao.
    pass


# ---------------------------------------------------------------------------
# 11. TRATAMENTO DE ERROS E BOAS PRATICAS
# ---------------------------------------------------------------------------
def exemplo_boas_praticas():
    """Reune um fluxo seguro para pequenos scripts."""
    from Bio.Seq import Seq

    entrada = "atgc"
    sequencia = Seq(entrada.upper().strip())

    if not sequencia:
        raise ValueError("A sequencia nao pode ser vazia.")
    if set(sequencia) - set("ACGTN"):
        raise ValueError("A sequencia possui simbolos fora do alfabeto esperado.")

    print("Entrada normalizada:", sequencia)
    print("Complemento reverso:", sequencia.reverse_complement())

    # Boas praticas:
    # - normalize maiusculas/minusculas antes de contar bases;
    # - documente se N e permitido;
    # - use with open(...) para fechar arquivos;
    # - confirme o formato antes de chamar SeqIO.parse;
    # - nao carregue arquivos enormes em list() sem necessidade;
    # - preserve id e descricao ao criar um novo SeqRecord;
    # - diferencie coordenadas de Python (0-based) das convencoes biologicas;
    # - mantenha os dados originais e salve resultados em outro arquivo.


def exemplo_pipeline_completo():
    """Modelo pequeno: ler, transformar, anotar e gravar."""
    from io import StringIO

    from Bio import SeqIO
    from Bio.Seq import Seq
    from Bio.SeqRecord import SeqRecord

    entrada = StringIO(">amostra_1 exemplo\nATGGCCTAA\n")
    saida = StringIO()

    resultados = []
    for registro in SeqIO.parse(entrada, "fasta"):
        registro.description += " | complemento reverso gerado"
        registro.seq = registro.seq.reverse_complement()
        resultados.append(registro)

    SeqIO.write(resultados, saida, "fasta")
    print("Resultado do pipeline:")
    print(saida.getvalue())

    # Em um arquivo real, troque StringIO por:
    # with open("entrada.fasta") as arquivo:
    #     registros = SeqIO.parse(arquivo, "fasta")
    #     ...
    #
    # Se for transformar a sequencia de um SeqRecord, mantenha os metadados
    # importantes e verifique se as features ainda fazem sentido na nova
    # orientacao.


# ---------------------------------------------------------------------------
# 12. DIFERENCAS ENTRE PYTHON PURO E BIOPYTHON
# ---------------------------------------------------------------------------
# str("ATGC") guarda texto, mas nao conhece biologia.
# Seq("ATGC") tambem guarda texto, mas oferece:
#     .complement(), .reverse_complement(), .transcribe(), .translate()
#
# list(SeqIO.parse(...)) carrega todos os registros na memoria.
# SeqIO.parse(...) retorna um iterador e permite processar um por vez.
#
# print(record.seq) mostra a sequencia.
# record.id, record.description e record.annotations mostram o contexto.
#
# Uma funcao Biopython pode retornar Seq, SeqRecord, Alignment, arvore ou
# outros objetos. Use type(resultado) e a documentacao para descobrir o tipo
# antes de chamar metodos de outra classe.


# ---------------------------------------------------------------------------
# 13. ERROS FREQUENTES
# ---------------------------------------------------------------------------
# ModuleNotFoundError: No module named 'Bio'
#     Instale no mesmo Python usado para executar o programa:
#     py -m pip install biopython
#
# FileNotFoundError
#     Confira a pasta e o nome do arquivo. Prefira pathlib.Path:
#     from pathlib import Path
#     caminho = Path("dados") / "sequencias.fasta"
#
# ValueError: No records found
#     SeqIO.read() exige exatamente um registro. Use parse() quando o arquivo
#     puder ter zero ou muitos registros.
#
# ValueError: More than one record found
#     O arquivo possui varios registros e foi usado read(). Troque por parse()
#     ou confirme que o arquivo deveria conter somente um registro.
#
# KeyError em letter_annotations["phred_quality"]
#     O registro nao possui qualidade, ou foi lido como FASTA em vez de FASTQ.
#
# Sequencia traduzida inesperada
#     Verifique se o tamanho e multiplo de tres, onde comeca o frame e qual
#     tabela genetica deve ser usada. translate(table=...) permite escolher
#     outra tabela quando a biologia do organismo exigir.
#
# Resultado de alinhamento inesperado
#     Confira match_score, mismatch_score, open_gap_score e
#     extend_gap_score. Essas escolhas afetam o resultado.
#
# Erro ao gravar GenBank
#     GenBank exige anotacoes e campos coerentes, como molecule_type em
#     record.annotations. Revise o SeqRecord antes de chamar SeqIO.write.


# ---------------------------------------------------------------------------
# 14. RESUMO DO FLUXO DE UM PROJETO
# ---------------------------------------------------------------------------
# 1. Defina a pergunta biologica.
# 2. Escolha o formato de entrada (FASTA, FASTQ, GenBank, PDB etc.).
# 3. Leia com a classe apropriada (SeqIO, PDBParser, AlignIO...).
# 4. Valide IDs, alfabeto, tamanho e qualidade.
# 5. Transforme ou analise os dados.
# 6. Preserve os metadados importantes.
# 7. Grave no formato adequado.
# 8. Registre parametros e versao do Biopython.
#
# Para trabalhos reprodutiveis, guarde o comando de instalacao, os arquivos
# de entrada, o script e as configuracoes usadas na analise.


# ---------------------------------------------------------------------------
# 15. OUTROS MODULOS IMPORTANTES
# ---------------------------------------------------------------------------
# Bio.Align          alinhamentos modernos e objetos Alignment.
# Bio.AlignIO        leitura e escrita de alinhamentos.
# Bio.Blast          acesso a resultados BLAST; para novos projetos, tambem
#                     considere executar ferramentas do BLAST separadamente.
# Bio.Entrez         consultas aos bancos do NCBI.
# Bio.ExPASy         acesso a servicos ExPASy.
# Bio.Graphics       desenhos de mapas e anotacoes.
# Bio.PDB            estruturas de proteinas e acidos nucleicos.
# Bio.Phylo          filogenia e arvores.
# Bio.SearchIO       leitura de resultados de buscas, como BLAST.
# Bio.Seq            operacoes em sequencias.
# Bio.SeqFeature     genes, CDS, localizacoes e outras features.
# Bio.SeqIO          entrada e saida de sequencias.
# Bio.SeqRecord      sequencias com metadados.
# Bio.motifs         motivos de sequencias.
# Bio.Restriction    enzimas e mapas de restricao.
# Bio.PopGen         analises de genetica de populacoes.
#
# Nem todo modulo deve ser usado sem consultar sua documentacao: formatos,
# escalas de qualidade, coordenadas e convencoes podem variar.


# ---------------------------------------------------------------------------
# EXECUCAO DOS EXEMPLOS LOCAIS
# ---------------------------------------------------------------------------
def executar():
    """Executa exemplos que nao precisam de arquivos externos ou internet."""
    try:
        import Bio  # noqa: F401
    except ImportError:
        print("Biopython nao esta instalado neste Python.")
        print("Instale com: py -m pip install biopython")
        return

    print("\n--- Seq ---")
    exemplo_seq()
    print("\n--- Bases e codons ---")
    exemplo_bases_e_codons()
    print("\n--- Validacao ---")
    exemplo_sequencia_invalida()
    print("\n--- SeqRecord ---")
    exemplo_seqrecord()
    print("\n--- SeqIO ---")
    exemplo_seqio()
    print("\n--- Filtragem ---")
    exemplo_filtrar_sequencias()
    print("\n--- Alinhamento ---")
    exemplo_alinhamento()
    print("\n--- Identidade ---")
    exemplo_identidade()
    print("\n--- Motifs ---")
    exemplo_motifs()
    print("\n--- Restriction ---")
    exemplo_restriction()
    print("\n--- Boas praticas ---")
    exemplo_boas_praticas()
    print("\n--- Pipeline completo ---")
    exemplo_pipeline_completo()
    print(
        "\nOs exemplos de FASTQ, GenBank, NCBI, PDB e filogenia "
        "estao nas funcoes acima."
    )


if __name__ == "__main__":
    executar()
