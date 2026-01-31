import { serve } from "https://deno.land/std@0.190.0/http/server.ts";
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2.58.0';
import { PDFDocument, rgb, StandardFonts } from 'https://esm.sh/pdf-lib@1.17.1';

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers":
    "authorization, x-client-info, apikey, content-type",
};

interface MedicalFormData {
  id: string;
  nome_completo: string;
  data_nascimento?: string;
  idade?: number;
  indicacao?: string;
  quem_indicou?: string;
  form_data: any;
}

const generatePDF = async (formData: MedicalFormData): Promise<Uint8Array> => {
  const data = formData.form_data;

  const pdfDoc = await PDFDocument.create();
  const timesRomanFont = await pdfDoc.embedFont(StandardFonts.TimesRoman);
  const timesRomanBold = await pdfDoc.embedFont(StandardFonts.TimesRomanBold);

  let page = pdfDoc.addPage([595, 842]);
  const { width, height } = page.getSize();
  let yPosition = height - 50;
  const margin = 50;
  const lineHeight = 14;
  const maxWidth = width - margin * 2;

  const addText = (text: string, fontSize: number, font: any, color = rgb(0, 0, 0)) => {
    if (yPosition < 80) {
      page = pdfDoc.addPage([595, 842]);
      yPosition = height - 50;
    }

    // Handle long text by wrapping
    const words = text.split(' ');
    let currentLine = '';
    const lines: string[] = [];

    for (const word of words) {
      const testLine = currentLine ? `${currentLine} ${word}` : word;
      const testWidth = font.widthOfTextAtSize(testLine, fontSize);

      if (testWidth > maxWidth && currentLine) {
        lines.push(currentLine);
        currentLine = word;
      } else {
        currentLine = testLine;
      }
    }
    if (currentLine) lines.push(currentLine);

    for (const line of lines) {
      if (yPosition < 80) {
        page = pdfDoc.addPage([595, 842]);
        yPosition = height - 50;
      }
      page.drawText(line, {
        x: margin,
        y: yPosition,
        size: fontSize,
        font: font,
        color: color,
      });
      yPosition -= lineHeight;
    }
  };

  const addSection = (title: string) => {
    yPosition -= 8;
    if (yPosition < 100) {
      page = pdfDoc.addPage([595, 842]);
      yPosition = height - 50;
    }
    addText(title, 13, timesRomanBold, rgb(0.15, 0.15, 0.4));
    yPosition -= 3;
  };

  const addField = (label: string, value: any) => {
    if (value === undefined || value === null || value === '') return;
    const text = `${label}: ${value}`;
    addText(text, 10, timesRomanFont);
  };

  const addFieldAlways = (label: string, value: any) => {
    const displayValue = (value === undefined || value === null || value === '') ? 'Não informado' : value;
    const text = `${label}: ${displayValue}`;
    addText(text, 10, timesRomanFont);
  };

  const addArrayField = (label: string, arr: string[]) => {
    if (!arr || !Array.isArray(arr)) return;
    const filtered = arr.filter(item => item && item.trim() !== '');
    if (filtered.length === 0) return;
    addText(`${label}:`, 10, timesRomanBold);
    filtered.forEach((item, index) => {
      addText(`  ${index + 1}. ${item}`, 10, timesRomanFont);
    });
  };

  // ============ HEADER ============
  addText('FORMULÁRIO MÉDICO COMPLETO', 16, timesRomanBold);
  addText(`Data de Geração: ${new Date().toLocaleDateString('pt-BR')}`, 10, timesRomanFont);
  yPosition -= 15;

  // ============ DADOS PESSOAIS ============
  addSection('DADOS PESSOAIS');
  addFieldAlways('Nome Completo', formData.nome_completo);
  addFieldAlways('Data de Nascimento', formData.data_nascimento);
  addFieldAlways('Idade', formData.idade ? `${formData.idade} anos` : null);
  addFieldAlways('Tipo de Indicação', formData.indicacao);
  addFieldAlways('Quem Indicou', formData.quem_indicou);

  // ============ SISTEMA RESPIRATÓRIO ============
  addSection('SISTEMA RESPIRATÓRIO');
  addFieldAlways('Asma ou Bronquite Asmática', data.asma);
  addField('  Observações', data.asmaObservacoes);
  addFieldAlways('Rinite Alérgica', data.rinite);
  addField('  Observações', data.riniteObservacoes);
  addFieldAlways('Sinusites', data.sinusites);
  addField('  Observações', data.sinusitesObservacoes);
  addFieldAlways('Enfisema', data.enfisema);
  addField('  Observações', data.enfisemaObservacoes);
  addFieldAlways('Enfisema/Bronquite Crônica', data.enfisemaBronquite);
  addField('  Observações', data.enfisemaBronquiteObservacoes);
  addFieldAlways('Pneumonias', data.pneumonias);
  addField('  Observações', data.pneumoniasObservacoes);
  addFieldAlways('Tuberculose', data.tuberculose);
  addField('  Observações', data.tuberculoseObservacoes);
  addFieldAlways('Outras Doenças Respiratórias', data.outrasRespiratorias);
  addField('  Observações', data.outrasRespiratoriasObservacoes);

  // ============ DISTÚRBIOS DO SONO ============
  addSection('DISTÚRBIOS DO SONO');
  addFieldAlways('Roncos ou Apneia do Sono', data.roncos);
  addField('  Frequência', data.roncosFrequencia);
  addField('  Intensidade', data.roncosIntensidade);
  addField('  Observações', data.roncosObservacoes);
  addFieldAlways('Insônia', data.insonia);
  addField('  Observações', data.insoniaObservacoes);
  addFieldAlways('Sonolência Diurna', data.sonolienciaDiurna);
  addField('  Observações', data.sonolienciaDiurnaObservacoes);
  addFieldAlways('Outros Problemas de Sono', data.outrosProblemasSono);
  addField('  Observações', data.outrosProblemasSonoObservacoes);

  // ============ ESCALA DE EPWORTH ============
  if (data.sonolienciaDiurna === 'Sim' || data.epworthTotal > 0) {
    addSection('ESCALA DE SONOLÊNCIA DE EPWORTH');
    addField('Lendo sentado', data.epworthLendo);
    addField('Assistindo TV', data.epworthTV);
    addField('Sentado em público', data.epworthPublico);
    addField('Como passageiro (1h)', data.epworthTransporte);
    addField('Descansando à tarde', data.epworthDescansando);
    addField('Conversando sentado', data.epworthConversando);
    addField('Após refeição sem álcool', data.epworthAposRefeicao);
    addField('Dirigindo parado no trânsito', data.epworthDirigindo);
    addText(`PONTUAÇÃO TOTAL: ${data.epworthTotal || 0} pontos`, 11, timesRomanBold);
  }

  // ============ SISTEMA CARDIOVASCULAR ============
  addSection('SISTEMA CARDIOVASCULAR');
  addFieldAlways('Pressão Alta (Hipertensão)', data.pressaoAlta);
  addField('  Observações', data.pressaoAltaObservacoes);
  addFieldAlways('Colesterol Alto', data.colesterolAlto);
  addField('  Observações', data.colesterolAltoObservacoes);
  addFieldAlways('Arritmias', data.arritmias);
  addField('  Observações', data.arritmiasObservacoes);
  addFieldAlways('Outros Problemas Cardíacos', data.outrosCardiacos);
  addField('  Observações', data.outrosCardiacosObservacoes);

  // ============ SISTEMA ENDÓCRINO ============
  addSection('SISTEMA ENDÓCRINO');
  addFieldAlways('Diabetes', data.diabetes);
  addField('  Observações', data.diabetesObservacoes);
  addFieldAlways('Problemas de Tireoide', data.tireoide);
  addField('  Observações', data.tireoideObservacoes);

  // ============ OUTROS SISTEMAS ============
  addSection('OUTROS SISTEMAS E CONDIÇÕES');
  addFieldAlways('Problemas Neurológicos', data.neurologicos);
  addField('  Observações', data.neurologicosObservacoes);
  addFieldAlways('Refluxo Gastroesofágico', data.refluxo);
  addField('  Observações', data.refluxoObservacoes);
  addFieldAlways('Problemas Intestinais', data.intestinais);
  addField('  Observações', data.intestinaisObservacoes);
  addFieldAlways('Problemas de Fígado', data.figado);
  addField('  Observações', data.figadoObservacoes);
  addFieldAlways('Problemas Urinários', data.urinarios);
  addField('  Observações', data.urinariosObservacoes);
  addFieldAlways('Problemas de Articulações/Ossos', data.articulacoes);
  addField('  Observações', data.articulacoesObservacoes);
  addFieldAlways('Problemas Psiquiátricos', data.psiquiatricos);
  addField('  Observações', data.psiquiatricosObservacoes);
  addFieldAlways('Tromboses', data.tromboses);
  addField('  Observações', data.trombosesObservacoes);
  addFieldAlways('Tumores/Câncer', data.tumores);
  addField('  Observações', data.tumoresObservacoes);
  addFieldAlways('Acidentes/Traumas', data.acidentes);
  addField('  Observações', data.acidentesObservacoes);
  addFieldAlways('Outros Problemas de Saúde', data.outrosProblemas);
  addField('  Observações', data.outrosProblemasObservacoes);

  // ============ TRANSFUSÃO ============
  addSection('TRANSFUSÃO SANGUÍNEA');
  addFieldAlways('Já recebeu transfusão', data.transfusao);
  addField('  Detalhes', data.transfusaoDetalhes);

  // ============ ALERGIAS ============
  addSection('ALERGIAS');
  addFieldAlways('Alergias a Medicamentos', data.alergiasMedicamentos);
  addField('  Medicamentos', data.alergiasMedicamentosLista);
  addFieldAlways('Alergias Respiratórias', data.alergiasRespiratorias);
  addField('  Especificar', data.alergiasRespiratoriasLista);
  addFieldAlways('Alergias Alimentares', data.alergiasAlimentares);
  addField('  Alimentos', data.alergiasAlimentaresLista);

  // ============ MEDICAÇÕES ============
  addSection('MEDICAÇÕES EM USO');
  if (data.medicacoes && Array.isArray(data.medicacoes)) {
    const meds = data.medicacoes.filter((m: string) => m && m.trim() !== '');
    if (meds.length > 0) {
      meds.forEach((med: string, index: number) => {
        addText(`  ${index + 1}. ${med}`, 10, timesRomanFont);
      });
    } else {
      addText('  Nenhuma medicação informada', 10, timesRomanFont);
    }
  } else {
    addText('  Nenhuma medicação informada', 10, timesRomanFont);
  }

  // ============ CIRURGIAS PRÉVIAS ============
  addSection('CIRURGIAS PRÉVIAS');
  if (data.cirurgias && Array.isArray(data.cirurgias)) {
    const cirurgiasList = data.cirurgias.filter((c: string) => c && c.trim() !== '');
    if (cirurgiasList.length > 0) {
      cirurgiasList.forEach((cirurgia: string, index: number) => {
        addText(`  ${index + 1}. ${cirurgia}`, 10, timesRomanFont);
      });
    } else {
      addText('  Nenhuma cirurgia informada', 10, timesRomanFont);
    }
  } else {
    addText('  Nenhuma cirurgia informada', 10, timesRomanFont);
  }

  // ============ HISTÓRIA FAMILIAR ============
  addSection('HISTÓRIA FAMILIAR');

  // Pai
  addFieldAlways('Pai', data.pai);
  addField('  Doenças conhecidas', data.paiDoencas);
  if (data.pai === 'Falecido') {
    addField('  Motivo do falecimento', data.paiMotivoFalecimento);
  }

  // Mãe
  addFieldAlways('Mãe', data.mae);
  addField('  Doenças conhecidas', data.maeDoencas);
  if (data.mae === 'Falecida') {
    addField('  Motivo do falecimento', data.maeMotivoFalecimento);
  }

  // Avós Paternos
  addFieldAlways('Avós Paternos', data.avosPaternos);
  addField('  Doenças conhecidas', data.avosPaternosDoencas);
  if (data.avosPaternos === 'Falecidos') {
    addField('  Motivo do falecimento', data.avosPaternosMotivo);
  }

  // Avós Maternos
  addFieldAlways('Avós Maternos', data.avosMaternos);
  addField('  Doenças conhecidas', data.avosMaternos_doencas);
  if (data.avosMaternos === 'Falecidos') {
    addField('  Motivo do falecimento', data.avosMaternos_motivo);
  }

  // Irmãos
  addFieldAlways('Irmãos', data.irmaos);
  addField('  Doenças conhecidas', data.irmaosDoencas);

  // Filhos
  addFieldAlways('Filhos', data.filhos);
  addField('  Doenças conhecidas', data.filhosDoencas);

  // Outros parentes
  addFieldAlways('Doenças importantes em outros parentes', data.outrosParentes);
  addField('  Detalhes', data.outrosParentesDetalhes);

  // ============ HÁBITOS - TABAGISMO ============
  addSection('HÁBITOS PESSOAIS - TABAGISMO');
  addFieldAlways('Fuma atualmente', data.fumaAtualmente);

  if (data.fumaAtualmente === 'Sim') {
    addField('  Tipo de fumo', data.tipoFumo);
    addField('  Idade que começou a fumar', data.idadeComecouFumar);
    addField('  Cigarros por dia', data.cigarrosPorDia);
    addField('  Carga Tabágica', data.cargaTabagica ? `${data.cargaTabagica} anos-maço` : null);
  }

  if (data.fumaAtualmente === 'Não') {
    addFieldAlways('Já fumou anteriormente', data.jaFumou);
    if (data.jaFumou === 'Sim') {
      addField('  Idade que começou', data.idadeComecouFumarEx);
      addField('  Idade que parou', data.idadeParouFumar);
      addField('  Cigarros por dia (na época)', data.cigarrosPorDiaEx);
      addField('  Carga Tabágica', data.cargaTabagica ? `${data.cargaTabagica} anos-maço` : null);
    }
  }

  addFieldAlways('Tabagismo passivo', data.tabagismoPassivo);
  addField('  Detalhes', data.tabagismoPassivoDetalhes);

  // ============ HÁBITOS - ÁLCOOL ============
  addSection('HÁBITOS PESSOAIS - ÁLCOOL');
  addFieldAlways('Consome álcool atualmente', data.consumeAlcool);

  if (data.consumeAlcool === 'Sim') {
    if (data.tiposAlcool && Array.isArray(data.tiposAlcool) && data.tiposAlcool.length > 0) {
      addField('  Tipos de bebida', data.tiposAlcool.join(', '));
    }
    addField('  Classificação do consumo', data.classificacaoConsumo);
    addField('  Observações', data.consumoObservacoes);
  }

  if (data.consumeAlcool === 'Não') {
    addFieldAlways('Já consumiu anteriormente', data.jaConsumiuAlcool);
  }

  // ============ ATIVIDADE FÍSICA ============
  addSection('ATIVIDADE FÍSICA');
  addFieldAlways('Pratica atividade física', data.atividadeFisica);

  if (data.atividadeFisica === 'Sim') {
    addField('  Tipo de atividade', data.tipoAtividade);
    addField('  Frequência semanal', data.frequenciaSemanal);
    addField('  Tempo total semanal', data.tempoTotalSemanal);
  }

  if (data.atividadeFisica === 'Não') {
    addFieldAlways('Já praticou anteriormente', data.atividadeFisicaPrevia);
  }

  // ============ ALIMENTAÇÃO ============
  addSection('ALIMENTAÇÃO');
  addFieldAlways('Tipo de alimentação', data.tipoAlimentacao);
  addField('  Especificar', data.tipoAlimentacaoEspecificar);

  // ============ VACINAÇÕES ============
  addSection('VACINAÇÕES');
  addFieldAlways('Vacina Influenza (Gripe)', data.influenza);
  addField('  Ano', data.influenzaAno);

  addFieldAlways('Vacina COVID-19', data.covid);
  addField('  Ano', data.covidAno);
  addField('  Número de doses', data.covidDoses);

  addFieldAlways('Vacina Pneumocócica', data.pneumococcica);
  addField('  Ano', data.pneumococcicaAno);
  if (data.tiposPneumococcica && Array.isArray(data.tiposPneumococcica) && data.tiposPneumococcica.length > 0) {
    addField('  Tipos', data.tiposPneumococcica.join(', '));
  }

  if (data.outrasVacinas && Array.isArray(data.outrasVacinas) && data.outrasVacinas.length > 0) {
    addField('Outras vacinas', data.outrasVacinas.join(', '));
  }
  addField('Outras vacinas (texto)', data.outrasVacinasTexto);

  // ============ RASTREAMENTOS ============
  addSection('RASTREAMENTOS / EXAMES PREVENTIVOS');
  if (data.colonoscopia) {
    addFieldAlways('Colonoscopia', data.colonoscopia);
    addField('  Ano', data.colonoscopiaAno);
  }
  if (data.mamografia) {
    addFieldAlways('Mamografia', data.mamografia);
    addField('  Ano', data.mamografiaAno);
  }
  if (data.exameUrologico) {
    addFieldAlways('Exame Urológico (PSA/Próstata)', data.exameUrologico);
    addField('  Ano', data.exameUrologicoAno);
  }

  // ============ OUTROS COMENTÁRIOS ============
  if (data.outrosComentarios && data.outrosComentarios.trim() !== '') {
    addSection('OUTROS COMENTÁRIOS');
    addText(data.outrosComentarios, 10, timesRomanFont);
  }

  // ============ DECLARAÇÃO LGPD ============
  addSection('DECLARAÇÃO LGPD');
  addText(data.declaracao ? 'Sim - Paciente autorizou o uso dos dados' : 'Não autorizado', 10, timesRomanFont);

  // ============ FOOTER ============
  yPosition = 40;
  page.drawText('Documento gerado automaticamente pelo sistema de formulários médicos', {
    x: margin,
    y: yPosition,
    size: 8,
    font: timesRomanFont,
    color: rgb(0.5, 0.5, 0.5),
  });
  page.drawText(`${new Date().toLocaleString('pt-BR')}`, {
    x: margin,
    y: yPosition - 10,
    size: 8,
    font: timesRomanFont,
    color: rgb(0.5, 0.5, 0.5),
  });

  return await pdfDoc.save();
};

const handler = async (req: Request): Promise<Response> => {
  console.log("Function invoked");

  if (req.method === "OPTIONS") {
    return new Response(null, { headers: corsHeaders });
  }

  try {
    const { formId } = await req.json();

    const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
    if (!formId || !uuidRegex.test(formId)) {
      console.log("Invalid form ID format");
      return new Response(
        JSON.stringify({ error: 'Invalid form ID format' }),
        { status: 400, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      );
    }

    console.log("Processing form ID:", formId);

    const supabaseUrl = Deno.env.get("SUPABASE_URL")!;
    const supabaseKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
    const supabase = createClient(supabaseUrl, supabaseKey);

    const { data: formData, error } = await supabase
      .from('medical_forms')
      .select('*')
      .eq('id', formId)
      .single();

    if (error) {
      console.error("Error fetching form data:", error);
      throw new Error(`Erro ao buscar dados do formulário`);
    }

    if (!formData) {
      throw new Error("Formulário não encontrado");
    }

    console.log("Form data fetched successfully for:", formData.nome_completo);
    console.log("Form data keys:", Object.keys(formData.form_data || {}));

    console.log("Generating PDF...");
    const pdfBytes = await generatePDF(formData);
    const pdfBase64 = btoa(String.fromCharCode(...pdfBytes));
    console.log("PDF generated successfully, size:", pdfBytes.length);

    const resendApiKey = Deno.env.get("RESEND_API_KEY");
    if (!resendApiKey) {
      throw new Error("RESEND_API_KEY não configurado");
    }

    const emailData = {
      from: "Formulário Médico <onboarding@resend.dev>",
      to: ["drfernandoazevedoconsultorio@gmail.com"],
      subject: `Novo Formulário Médico - ${formData.nome_completo}`,
      html: `
        <h2>Novo Formulário Médico Recebido</h2>
        <p><strong>Paciente:</strong> ${formData.nome_completo}</p>
        <p><strong>Data de Nascimento:</strong> ${formData.data_nascimento || 'Não informado'}</p>
        <p><strong>Idade:</strong> ${formData.idade || 'Não informado'} anos</p>
        <p><strong>Data de Preenchimento:</strong> ${new Date().toLocaleString('pt-BR')}</p>
        
        <h3>Resumo:</h3>
        <ul>
          <li><strong>Indicação:</strong> ${formData.indicacao || 'Não informado'}</li>
          <li><strong>Quem indicou:</strong> ${formData.quem_indicou || 'Não informado'}</li>
        </ul>
        
        <p><strong>O formulário completo está anexo em PDF.</strong></p>
        <p style="color: #666; font-size: 12px;">Este é um email automático gerado pelo sistema de formulários médicos.</p>
      `,
      attachments: [
        {
          filename: `formulario-medico-${formData.nome_completo.replace(/\s+/g, '-')}.pdf`,
          content: pdfBase64,
        },
      ],
    };

    const emailResponse = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${resendApiKey}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(emailData),
    });

    if (!emailResponse.ok) {
      const errorText = await emailResponse.text();
      console.error("Resend API error:", errorText);
      throw new Error(`Erro ao enviar email: ${emailResponse.status} - ${errorText}`);
    }

    const emailResult = await emailResponse.json();
    console.log("Email sent successfully:", emailResult);

    return new Response(
      JSON.stringify({
        success: true,
        message: "Email com dados do formulário enviado com sucesso",
        emailId: emailResult.id
      }),
      {
        status: 200,
        headers: {
          "Content-Type": "application/json",
          ...corsHeaders,
        },
      }
    );
  } catch (error: any) {
    console.error("Error in send-medical-form-pdf function:", error);
    return new Response(
      JSON.stringify({
        success: false,
        error: error.message
      }),
      {
        status: 500,
        headers: {
          "Content-Type": "application/json",
          ...corsHeaders
        },
      }
    );
  }
};

serve(handler);
