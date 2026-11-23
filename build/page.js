function derive(years) {
  const base = years[0];
  const baseBps = base.budget / base.enrollment;
  let lastEnroll = null;
  const ref = years.filter(function (x) { return x.fy === '2024-25'; })[0];
  return years.map(function (r) {
    const hasActual = r.actual_recurring != null;
    const spendVal = hasActual ? r.actual_recurring : r.budget;
    const spendBase = hasActual ? base.actual_recurring : base.budget;
    if (r.enrollment != null) lastEnroll = r.enrollment;
    const bps = r.budget / (r.enrollment != null ? r.enrollment : lastEnroll);
    const rec = r.actual_recurring;
    const hasFn = rec != null && r.fn_reg != null;
    const instr = hasFn ? r.fn_reg + r.fn_spec + r.fn_voc + r.fn_oi : null;
    const supp = hasFn ? r.fn_ss + r.fn_isup : null;
    const adm = hasFn ? r.fn_gab + r.fn_sadm + r.fn_bus : null;
    const hasRev = r.rev_tot != null;
    const stateAid = hasRev ? r.rev_adeq + r.rev_ostate : null;
    var av = function (a) { var v = a.filter(function (x) { return x != null; }); return v.length === a.length ? v.reduce(function (p, c) { return p + c; }, 0) / v.length : null; };
    var o = {
      fy: r.fy,
      f_cpi: ref.cpi_ne / r.cpi_ne,
      f_eci: ref.eci_edu / r.eci_edu,
      spend_value: spendVal,
      spend_basis: hasActual ? 'Actual' : 'Adopted budget',
      spend_delta_pct: (spendVal / spendBase - 1) * 100,
      enrollment_delta_pct: r.enrollment != null ? (r.enrollment / base.enrollment - 1) * 100 : null,
      budget_per_student: bps,
      bps_basis: r.enrollment != null ? 'October 1 enrollment' : 'Latest enrollment on file',
      bps_delta_pct: (bps / baseBps - 1) * 100,
      cpp_delta_pct: r.nhed_cpp != null ? (r.nhed_cpp / base.nhed_cpp - 1) * 100 : null,
      ela_delta_pts: r.ela != null ? r.ela - base.ela : null,
      math_delta_pts: r.math != null ? r.math - base.math : null,
      sci_delta_pts: r.sci != null ? r.sci - base.sci : null,
      instr_amt: instr,
      supp_amt: supp,
      adm_amt: adm,
      instr_share: hasFn ? instr / rec * 100 : null,
      supp_share: hasFn ? supp / rec * 100 : null,
      adm_share: hasFn ? adm / rec * 100 : null,
      plant_share: hasFn ? r.fn_plant / rec * 100 : null,
      trans_share: hasFn ? r.fn_trans / rec * 100 : null,
      debt_share: hasFn ? r.fn_bint / rec * 100 : null,
      food_share: hasFn ? r.fn_food / rec * 100 : null,
      ben_load: r.instr_sal != null ? r.instr_ben / r.instr_sal * 100 : null,
      ben_load_delta: r.instr_sal != null ? r.instr_ben / r.instr_sal * 100 - base.instr_ben / base.instr_sal * 100 : null,
      state_aid_amt: stateAid,
      local_share: hasRev ? r.rev_local / r.rev_tot * 100 : null,
      state_share: hasRev ? stateAid / r.rev_tot * 100 : null,
      fed_share: hasRev ? r.rev_fed / r.rev_tot * 100 : null,
      other_share: hasRev ? r.rev_oth_local / r.rev_tot * 100 : null,
      spec_pps: hasFn && r.enrollment != null ? r.fn_spec / r.enrollment : null,
      spec_share: hasFn ? r.fn_spec / rec * 100 : null,
      plant_pps: hasFn && r.enrollment != null ? r.fn_plant / r.enrollment : null,
      trans_pps: hasFn && r.enrollment != null ? r.fn_trans / r.enrollment : null,
      debt_pps: hasFn && r.enrollment != null ? r.fn_bint / r.enrollment : null,
      local_pps: hasRev && r.enrollment != null ? r.rev_local / r.enrollment : null,
      state_pps: hasRev && r.enrollment != null ? stateAid / r.enrollment : null,
      adq_pct: r.adq_total != null ? r.adq_total / r.adq_cost * 100 : null,
      adq_swept_pct: r.adq_total != null ? r.adq_swept / r.adq_total * 100 : null,
      adq_extra: r.adq_total != null ? r.adq_total - r.adq_cost : null,
      cpp_vs_avg: r.nhed_cpp != null && r.cpp_state_avg != null ? (r.nhed_cpp / r.cpp_state_avg - 1) * 100 : null,
      cpp_vs_med: r.nhed_cpp != null && r.cpp_k12_med != null ? (r.nhed_cpp / r.cpp_k12_med - 1) * 100 : null,
      t_start: r.t_start, t_start_state: r.t_start_state, t_avg: r.t_avg, t_avg_state: r.t_avg_state, t_avg_file: r.t_avg_file, t_avg_fte: r.t_avg_fte, t_avg_note: r.t_avg_note,
      ratio: r.ratio, ratio_state: r.ratio_state, ratio_teachers: r.ratio_teachers, ratio_enr: r.ratio_enr,
      eq_tot: r.eq_tot, eq_dur: r.eq_dur, eq_lee: r.eq_lee, eq_mad: r.eq_mad,
      levy_tot: r.levy_tot, levy_dur: r.levy_dur, levy_lee: r.levy_lee, levy_mad: r.levy_mad,
      eq_pps: r.eq_tot != null && r.enrollment != null ? r.eq_tot / r.enrollment : null,
      eff_rate: r.eq_tot != null ? r.levy_tot / r.eq_tot * 1000 : null,
      lsh_dur: r.levy_tot != null ? r.levy_dur / r.levy_tot * 100 : null,
      lsh_lee: r.levy_tot != null ? r.levy_lee / r.levy_tot * 100 : null,
      lsh_mad: r.levy_tot != null ? r.levy_mad / r.levy_tot * 100 : null,
      vsh_dur: r.eq_tot != null ? r.eq_dur / r.eq_tot * 100 : null,
      vsh_lee: r.eq_tot != null ? r.eq_lee / r.eq_tot * 100 : null,
      vsh_mad: r.eq_tot != null ? r.eq_mad / r.eq_tot * 100 : null
    };
    ['dur', 'lee', 'mad'].forEach(function (t) {
      var sf = r.fv_dur + r.fv_lee + r.fv_mad, sa = r.adm_dur + r.adm_lee + r.adm_mad;
      o['vf_' + t] = r['fv_' + t] / sf * 100;
      o['af_' + t] = r['adm_' + t] / sa * 100;
      var has = r.levy_dur != null;
      o['eff_' + t] = has ? r['levy_' + t] / r['eq_' + t] * 1000 : null;
      o['pps_' + t] = has ? r['levy_' + t] / r['adm_' + t] : null;
      o['crs_' + t] = has ? r['cr_' + t] / (r['levy_' + t] + r['cr_' + t]) * 100 : null;
      o['sch_' + t] = has && r['ssr_' + t] != null && r['tt_' + t] != null ? (r['tax_' + t] + r['ssr_' + t]) / r['tt_' + t] * 100 : null;
      o['oth_' + t] = has && r['ssr_' + t] != null && r['tt_' + t] != null ? r['tt_' + t] - r['tax_' + t] - r['ssr_' + t] : null;
    });
    o.cs_d = av([r.cs_mw12, r.cs_mo12, r.cs_mw34, r.cs_mo34]);
    o.cs_st = av([r.cs_st12, r.cs_st34]);
    o.sat_tot = r.sat_rw != null ? r.sat_rw + r.sat_m : null;
    o.sat_nh_tot = r.sat_rw_nh != null ? r.sat_rw_nh + r.sat_m_nh : null;
    o.sp_share = r.sp_tot != null && r.enrollment != null ? r.sp_tot / r.enrollment * 100 : null;
    o.frl_share = r.frl != null && r.enrollment != null ? r.frl / r.enrollment * 100 : null;
    o.ell_share = r.ell != null && r.enrollment != null ? r.ell / r.enrollment * 100 : null;
    o.efa_tot = r.efa_dur != null ? r.efa_dur + r.efa_lee + r.efa_mad : null;
    o.inc_ser = r.vio_inj != null ? r.vio_inj + r.vio_non + r.weap + r.drug + r.alc + r.vio_oth : null;
    o.td_adv = r.td_m != null ? r.td_m + r.td_x : null;
    o.td_adv_nh = r.td_m_nh != null ? r.td_m_nh + r.td_x_nh : null;
    o.tx_tot = av([r.tx_mw, r.tx_mo, r.tx_ms, r.tx_hs]) != null ? r.tx_mw + r.tx_mo + r.tx_ms + r.tx_hs : null;
    o.at_d = av([r.at_k, r.at_e, r.at_m, r.at_h]);
    o.at_s = av([r.at_k_nh, r.at_e_nh, r.at_m_nh, r.at_h_nh]);
    return o;
  });
}

function headline(years) {
  const base = years[0];
  const actual = years.filter(function (r) { return r.actual_recurring != null; });
  const enr = years.filter(function (r) { return r.enrollment != null; });
  const ela = years.filter(function (r) { return r.ela != null; });
  const lastA = actual[actual.length - 1];
  const lastE = enr[enr.length - 1];
  const rc = (base.cpi_ne / lastA.cpi_ne), re = (base.eci_edu / lastA.eci_edu);
  return [{
    spend_pct: (lastA.actual_recurring / base.actual_recurring - 1) * 100,
    spend_cpi_pct: (lastA.actual_recurring / base.actual_recurring * rc - 1) * 100,
    spend_eci_pct: (lastA.actual_recurring / base.actual_recurring * re - 1) * 100,
    cpp_pct: (lastA.nhed_cpp / base.nhed_cpp - 1) * 100,
    cpp_cpi_pct: (lastA.nhed_cpp / base.nhed_cpp * rc - 1) * 100,
    cpp_eci_pct: (lastA.nhed_cpp / base.nhed_cpp * re - 1) * 100,
    enrollment_pct: (lastE.enrollment / base.enrollment - 1) * 100,
    ela_min: Math.min.apply(null, ela.map(function (r) { return r.ela; })),
    ela_max: Math.max.apply(null, ela.map(function (r) { return r.ela; })),
    state_min: Math.min.apply(null, ela.map(function (r) { return r.ela_state; })),
    state_max: Math.max.apply(null, ela.map(function (r) { return r.ela_state; }))
  }];
}

dash.calc('derived', {
  inputs: ['years'],
  fn: derive,
  title: 'Year-by-year changes',
  description: 'Spending basis, changes since FY 2017-18, budget per student, spending mix and revenue mix, worked out from the ten-year record.'
});
dash.calc('headline', {
  inputs: ['years'],
  fn: headline,
  title: 'Headline changes',
  description: 'Change in actual spending, cost per pupil (nominal and inflation-adjusted) and enrollment since FY 2017-18, and the range of reading proficiency.'
});

(function () {
  var NS = 'http://www.w3.org/2000/svg';
  var sel = 7;
  var mode = 'nom';
  var MODES = { nom: { label: 'Nominal dollars', f: null }, cpi: { label: 'Northeast CPI-U', f: 'f_cpi', idx: 'cpi_ne', n: 'cpi_ne_months', nn: 12 }, eci: { label: 'education labor costs (ECI)', f: 'f_eci', idx: 'eci_edu', n: 'eci_quarters', nn: 4 } };
  var MONEY = ['fb_tot', 'fb_un', 'fb_com', 'instr_sal', 'instr_ben', 'actual_recurring', 'actual_total', 'construction', 'budget', 'budget_per_student', 'nhed_cpp', 'cpp_el', 'cpp_ms', 'cpp_hs', 'spend_value', 'instr_amt', 'supp_amt', 'adm_amt', 'state_aid_amt', 'fn_reg', 'fn_spec', 'fn_voc', 'fn_oi', 'fn_ss', 'fn_isup', 'fn_gab', 'fn_sadm', 'fn_bus', 'fn_plant', 'fn_trans', 'fn_bint', 'fn_food', 'rev_local', 'rev_oth_local', 'rev_adeq', 'rev_ostate', 'rev_fed', 'rev_tot', 'spec_pps', 'plant_pps', 'trans_pps', 'debt_pps', 'local_pps', 'state_pps', 'adq_cost', 'adq_swept', 'adq_total', 'adq_extra', 'adq_base', 'adq_fr', 'adq_sped', 'adq_ell', 'adq_home', 'cpp_state_avg', 'cpp_k12_med', 'pps_dur', 'pps_lee', 'pps_mad', 'bld_aid', 'sp_ent', 'sp_paid', 'sp_cost', 'cte_tt', 'efa_po', 't_start', 't_start_state', 't_avg', 't_avg_state'];
  var NAMES = ['spend', 'students', 'budget', 'ela', 'cpp', 'instr', 'local', 'math', 'sci', 'ben', 'fed', 'rate', 'sgp', 'grp', 'att', 'lvl', 'spec', 'adm', 'bldg', 'pay', 'aid', 'cmp', 'staff', 'share', 'base', 'tstart', 'tavg', 'ratio', 'lvlenr', 'fb', 'cls', 'sat', 'coll', 'sped', 'frl', 'ell', 'efa', 'drop', 'ctc', 'tdeg', 'texp', 'attlvl', 'proj', 'app', 'eff', 'sch', 'cred', 'pps3', 'vote', 'bldaid', 'spedaid', 'trunt', 'susp', 'bully', 'viol', 'restr', 'grad', 'part'];

  function svgEl(tag, attrs, parent) {
    var e = document.createElementNS(NS, tag);
    var k;
    for (k in (attrs || {})) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  }
  function div(cls, text) {
    var d = document.createElement('div');
    if (cls) d.className = cls;
    if (text != null) d.textContent = text;
    return d;
  }
  function money(v) { return '$' + Math.round(v).toLocaleString('en-US'); }
  function moneyM(v, d) { return '$' + (v / 1e6).toFixed(d == null ? 1 : d) + 'M'; }
  function num(v) { return Math.round(v).toLocaleString('en-US'); }
  function signPct(v) { return (v >= 0 ? '+' : '−') + Math.abs(v).toFixed(1) + '%'; }
  function arrow(v) { return v > 0 ? '▲' : (v < 0 ? '▼' : '▬'); }
  function deltaPct(v) { return arrow(v) + ' ' + Math.abs(v).toFixed(1) + '%'; }

  function getData() {
    var y = dash.data('years');
    var d = dash.data('derived');
    if (y.status !== 'ok' || d.status !== 'ok' || !y.data.length || y.data.length !== d.data.length) return null;
    var out = y.data.map(function (r, i) { return Object.assign({}, r, d.data[i]); });
    if (mode !== 'nom') {
      var M = MODES[mode];
      out.forEach(function (r) {
        var f = r[M.f];
        r.partial = r[M.n] < M.nn;
        r.n_used = r[M.n];
        MONEY.forEach(function (k) { if (r[k] != null) r[k] = r[k] * f; });
      });
      var b = out[0];
      out.forEach(function (r) {
        r.spend_delta_pct = (r.spend_value / (r.actual_recurring != null ? b.actual_recurring : b.budget) - 1) * 100;
        r.bps_delta_pct = (r.budget_per_student / b.budget_per_student - 1) * 100;
        r.cpp_delta_pct = r.nhed_cpp != null ? (r.nhed_cpp / b.nhed_cpp - 1) * 100 : null;
      });
    }
    D0 = out[0];
    return out;
  }

  function stat(r) {
    if (r.status === 'provisional') return 'Provisional: budget voted March 2026';
    if (r.status === 'budget') return 'Budget adopted; actual spending not yet filed';
    return 'Actual results';
  }

  var BASE = 'FY 2017-18';
  var FIRST = '2017-18';
  function baseOr(r, txt) { return r.fy === FIRST ? 'Base year' : txt; }
  function pts(d) { return d === 0 ? '▬ No change' : arrow(d) + ' ' + Math.abs(d) + ' point' + (Math.abs(d) === 1 ? '' : 's'); }
  function pct1(v) { return v.toFixed(1) + '%'; }

  function testRow(opts) {
    // opts: field, stateField, deltaField, aria, domain, ticks, noun
    var f = opts.field, sf = opts.stateField;
    return {
      aria: opts.aria,
      domain: opts.domain,
      ticks: opts.ticks,
      axis: !!opts.axis,
      noTestMark: true,
      tickFmt: function (v) { return v + '%'; },
      series: [
        { id: 'state', get: function (r) { return r[sf]; }, comp: true },
        { id: f, get: function (r) { return r[f]; }, main: true }
      ],
      label: function (r) {
        if (r.no_test) return { big: '—', sub: 'No statewide results for 2019-20', delta: '', tag: 'No test', prov: true, src: 'years', field: f };
        if (r[f] == null) return { big: '—', sub: 'Results not yet available', delta: '', tag: 'Provisional', prov: true, src: 'years', field: f };
        return {
          big: r[f] + '%',
          sub: 'Share proficient (' + opts.noun + '), all tested grades',
          delta: baseOr(r, pts(r[opts.deltaField]) + ' since ' + BASE),
          tag: 'Actual', prov: false, src: 'years', field: f
        };
      },
      tip: function (r) {
        if (r.no_test) return { lines: [[opts.noun, 'not tested']], note: 'No statewide results were published for 2019-20.' };
        if (r[f] == null) return { lines: [[opts.noun, 'not yet available']], note: 'Spring 2027 results are not out.' };
        var l = [['Oyster River', r[f] + '%'], ['New Hampshire', r[sf] + '%']];
        if (opts.part && r.ela_part != null) l.push(['Participation', r.ela_part + '% (state ' + r.ela_state_part + '%)']);
        return { lines: l, note: 'Source: NH DOE state assessment files, levels 3 and 4.' };
      }
    };
  }

  var ROWS = {
    spend: {
      money: true,
      aria: 'Spending by fiscal year: actual operating expenditure and adopted budget',
      domain: [40e6, 65e6],
      ticks: [40e6, 50e6, 60e6],
      tickFmt: function (v) { return '$' + (v / 1e6) + 'M'; },
      series: [
        { id: 'budget', get: function (r) { return r.budget; }, comp: true },
        { id: 'actual', get: function (r) { return r.actual_recurring; }, main: true }
      ],
      label: function (r) {
        var budgetBasis = r.spend_basis !== 'Actual';
        return {
          big: moneyM(r.spend_value, 1),
          sub: budgetBasis ? 'Adopted budget, all funds' : 'Operating expenditure, DOE-25',
          delta: baseOr(r, deltaPct(r.spend_delta_pct) + ' since ' + BASE + (budgetBasis ? ' (budget basis)' : '')),
          tag: budgetBasis ? (r.status === 'provisional' ? 'Provisional' : 'Budget') : 'Actual',
          prov: budgetBasis,
          src: 'derived', field: 'spend_value'
        };
      },
      tip: function (r) {
        var l = [];
        if (r.actual_recurring != null) {
          l.push(['Operating spending', money(r.actual_recurring)]);
          l.push(['Incl. construction', money(r.actual_total)]);
        } else {
          l.push(['Operating spending', 'not yet filed']);
          if (r.fy === '2025-26') l.push(['Prelim. general fund under budget by', '$584,435']);
        }
        l.push(['Adopted budget', (r.budget_approx ? '≈ ' : '') + money(r.budget)]);
        return { lines: l, note: r.budget_approx ? 'FY 2017-18 budget is approximate (rounded to $43.8M in the only source found).' : (r.fy === '2025-26' ? 'The DOE-25 for 2025-26 is not filed yet. The district’s preliminary June 30, 2026 report (unaudited) shows general fund expenditures $584,435 under budget and revenue $431,518 above spending before using fund balance. Source: ORCSD financial report, June 2026.' : 'Source: DOE-25 filings (NH DOE); ballot budget article.') };
      }
    },
    students: {
      aria: 'October 1 student headcount by fiscal year',
      domain: [2000, 2200],
      ticks: [2000, 2100, 2200],
      tickFmt: function (v) { return v.toLocaleString('en-US'); },
      series: [{ id: 'enr', get: function (r) { return r.enrollment; }, main: true }],
      label: function (r) {
        if (r.enrollment == null) return { big: '—', sub: 'No district-wide projection sourced yet', delta: '', tag: 'Provisional', prov: true, src: 'years', field: 'enrollment' };
        return {
          big: num(r.enrollment),
          sub: 'October 1 headcount',
          delta: baseOr(r, deltaPct(r.enrollment_delta_pct) + ' since ' + BASE),
          tag: 'Actual', prov: false, src: 'years', field: 'enrollment'
        };
      },
      tip: function (r) {
        return {
          lines: [['October 1 headcount', r.enrollment != null ? num(r.enrollment) : 'no projection on file']],
          note: r.fy === '2026-27' ? 'District October 1, 2026 count from the October 7 board packet (2,026 in classrooms; 2,037 including home-educated students). NH DOE has not published its figure.' : 'Source: NH DOE fall enrollment, via the district 2026 Annual Report.'
        };
      }
    },
    budget: {
      money: true,
      aria: 'Adopted budget per student by fiscal year',
      domain: [20000, 32500],
      ticks: [20000, 25000, 30000],
      tickFmt: function (v) { return '$' + v.toLocaleString('en-US'); },
      series: [{ id: 'bps', get: function (r) { return r.budget_per_student; }, main: true, prov: function (r) { return r.enrollment == null || r.budget_approx; } }],
      label: function (r) {
        var soft = r.enrollment == null || r.budget_approx;
        return {
          big: (r.budget_approx ? '≈ ' : '') + money(r.budget_per_student),
          sub: r.enrollment != null ? 'Adopted budget ÷ October 1 enrollment' : 'Adopted budget ÷ latest enrollment on file',
          delta: baseOr(r, deltaPct(r.bps_delta_pct) + ' since ' + BASE),
          tag: r.budget_approx ? 'Approximate' : (r.enrollment != null ? 'Budget' : 'Provisional'), prov: true,
          src: 'derived', field: 'budget_per_student'
        };
      },
      tip: function (r) {
        var l = [['Adopted budget', (r.budget_approx ? '≈ ' : '') + money(r.budget)], ['Enrollment used', num(r.enrollment != null ? r.enrollment : 2038)]];
        l.push(['Budget per student', money(r.budget_per_student)]);
        if (r.nhed_cpp != null) l.push(['NH DOE actual cost per pupil', money(r.nhed_cpp)]);
        return { lines: l, note: 'Budget ÷ enrollment. The NH DOE figure is actual spending per average daily membership.' };
      }
    },
    ela: testRow({ field: 'ela', stateField: 'ela_state', deltaField: 'ela_delta_pts', noun: 'ELA', part: true, axis: true, domain: [45, 85], ticks: [50, 60, 70, 80], aria: 'Share of students proficient in English language arts, Oyster River and New Hampshire' }),
    cpp: {
      money: true,
      aria: 'Actual current expenditure per pupil by fiscal year',
      domain: [15000, 26000],
      ticks: [15000, 20000, 25000],
      tickFmt: function (v) { return '$' + v.toLocaleString('en-US'); },
      series: [{ id: 'cpp', get: function (r) { return r.nhed_cpp; }, main: true }],
      label: function (r) {
        if (r.nhed_cpp == null) return { big: '—', sub: 'Not yet filed with the NH DOE', delta: '', tag: 'Pending', prov: true, src: 'years', field: 'nhed_cpp' };
        return {
          big: money(r.nhed_cpp),
          sub: 'Current expenditure per pupil, NH DOE',
          delta: baseOr(r, deltaPct(r.cpp_delta_pct) + ' since ' + BASE),
          tag: 'Actual', prov: false, src: 'years', field: 'nhed_cpp'
        };
      },
      tip: function (r) {
        if (r.nhed_cpp == null) return { lines: [['Cost per pupil', 'not yet filed']], note: 'Appears after the district files its DOE-25.' };
        return {
          lines: [['District total', money(r.nhed_cpp)], ['Elementary', money(r.cpp_el)], ['Middle', money(r.cpp_ms)], ['High school', money(r.cpp_hs)]],
          note: 'Source: DOE-25 District Profile (NH DOE). Excludes construction and bond principal.'
        };
      }
    },
    instr: {
      aria: 'Share of operating spending going to instruction, by fiscal year',
      domain: [50, 70],
      ticks: [50, 55, 60, 65],
      tickFmt: function (v) { return v + '%'; },
      series: [{ id: 'instr', get: function (r) { return r.instr_share; }, main: true }],
      label: function (r) {
        if (r.instr_share == null) return { big: '—', sub: 'Not yet filed with the NH DOE', delta: '', tag: 'Pending', prov: true, src: 'derived', field: 'instr_share' };
        return {
          big: pct1(r.instr_share),
          sub: 'Instruction ÷ operating spending',
          delta: baseOr(r, (Math.abs(r.instr_share - D0.instr_share) < 0.05 ? '▬ No change' : arrow(r.instr_share - D0.instr_share) + ' ' + Math.abs(r.instr_share - D0.instr_share).toFixed(1) + ' points') + ' since ' + BASE),
          tag: 'Actual', prov: false, src: 'derived', field: 'instr_share'
        };
      },
      tip: function (r) {
        if (r.instr_share == null) return { lines: [['Spending mix', 'not yet filed']], note: 'Appears after the district files its DOE-25.' };
        function ln(name, amt, sh) { return [name, moneyM(amt, 1) + ' · ' + sh.toFixed(1) + '%']; }
        return {
          lines: [
            ln('Instruction', r.instr_amt, r.instr_share),
            ln('Student & staff support', r.supp_amt, r.supp_share),
            ln('Administration & business', r.adm_amt, r.adm_share),
            ln('Plant operations', r.fn_plant, r.plant_share),
            ln('Transportation', r.fn_trans, r.trans_share),
            ln('Debt interest', r.fn_bint, r.debt_share),
            ln('Food service', r.fn_food, r.food_share)
          ],
          note: 'Share of total recurring expenditures. Source: DOE-25 District Profile.'
        };
      }
    },
    local: {
      aria: 'Local property tax and state aid as shares of district revenue, by fiscal year',
      domain: [10, 85],
      ticks: [20, 40, 60, 80],
      tickFmt: function (v) { return v + '%'; },
      series: [
        { id: 'state', get: function (r) { return r.state_share; }, comp: true },
        { id: 'local', get: function (r) { return r.local_share; }, main: true }
      ],
      label: function (r) {
        if (r.local_share == null) return { big: '—', sub: 'Not yet filed with the NH DOE', delta: '', tag: 'Pending', prov: true, src: 'derived', field: 'local_share' };
        return {
          big: pct1(r.local_share),
          sub: 'Local property tax ÷ total revenue',
          delta: baseOr(r, (arrow(r.local_share - D0.local_share) + ' ' + Math.abs(r.local_share - D0.local_share).toFixed(1) + ' points') + ' since ' + BASE),
          tag: 'Actual', prov: false, src: 'derived', field: 'local_share'
        };
      },
      tip: function (r) {
        if (r.local_share == null) return { lines: [['Revenue mix', 'not yet filed']], note: 'Appears after the district files its DOE-25.' };
        return {
          lines: [
            ['Local property tax', moneyM(r.rev_local, 1) + ' · ' + r.local_share.toFixed(1) + '%'],
            ['State aid', moneyM(r.state_aid_amt, 1) + ' · ' + r.state_share.toFixed(1) + '%'],
            ['Federal aid', moneyM(r.rev_fed, 1) + ' · ' + r.fed_share.toFixed(1) + '%'],
            ['Tuition, food, other local', moneyM(r.rev_oth_local, 1) + ' · ' + r.other_share.toFixed(1) + '%']
          ],
          note: 'Share of total revenues of ' + moneyM(r.rev_tot, 1) + '. Source: DOE-25 District Profile.'
        };
      }
    },
    math: testRow({ field: 'math', stateField: 'math_state', deltaField: 'math_delta_pts', noun: 'math', axis: false, domain: [30, 80], ticks: [40, 50, 60, 70], aria: 'Share of students proficient in math, Oyster River and New Hampshire' }),
    sci: testRow({ field: 'sci', stateField: 'sci_state', deltaField: 'sci_delta_pts', noun: 'science', axis: true, domain: [30, 70], ticks: [40, 50, 60], aria: 'Share of students proficient in science, Oyster River and New Hampshire' })
  };

  ROWS.ben = {
    aria: 'Instruction staff benefits as a percent of salaries, by fiscal year',
    domain: [40, 55], ticks: [40, 45, 50], axis: false,
    tickFmt: function (v) { return v + '%'; },
    series: [{ id: 'ben', get: function (r) { return r.ben_load; }, main: true }],
    label: function (r) {
      if (r.ben_load == null) return { big: '—', sub: 'Not yet filed with the NH DOE', delta: '', tag: 'Pending', prov: true, src: 'derived', field: 'ben_load' };
      var d = r.ben_load_delta;
      return {
        big: pct1(r.ben_load), sub: 'Benefits ÷ salaries, instructional staff',
        delta: baseOr(r, arrow(d) + ' ' + Math.abs(d).toFixed(1) + ' points since ' + BASE),
        tag: 'Actual', prov: false, src: 'derived', field: 'ben_load'
      };
    },
    tip: function (r) {
      if (r.ben_load == null) return { lines: [['Salaries and benefits', 'not yet filed']], note: 'Appears after the district files its DOE-25.' };
      return {
        lines: [['Salaries', money(r.instr_sal)], ['Benefits', money(r.instr_ben)], ['Benefits per $1 of salary', '$' + (r.instr_ben / r.instr_sal).toFixed(2)]],
        note: 'Instruction accounts 1100 to 1400, general and special revenue funds. Source: DOE-25 Salaries-Benefits sheet.'
      };
    }
  };
  ROWS.fed = {
    money: true,
    aria: 'Federal aid received by fiscal year',
    domain: [0, 2.6e6], ticks: [0, 1e6, 2e6], axis: false,
    tickFmt: function (v) { return '$' + (v / 1e6).toFixed(1) + 'M'; },
    series: [{ id: 'fed', get: function (r) { return r.rev_fed; }, main: true }],
    label: function (r) {
      if (r.rev_fed == null) return { big: '—', sub: 'Not yet filed with the NH DOE', delta: '', tag: 'Pending', prov: true, src: 'years', field: 'rev_fed' };
      return {
        big: '$' + (r.rev_fed / 1e6).toFixed(2) + 'M', sub: 'Federal aid received',
        delta: baseOr(r, deltaPct((r.rev_fed / D0.rev_fed - 1) * 100) + ' since ' + BASE),
        tag: 'Actual', prov: false, src: 'years', field: 'rev_fed'
      };
    },
    tip: function (r) {
      if (r.rev_fed == null) return { lines: [['Federal aid', 'not yet filed']], note: 'Appears after the district files its DOE-25.' };
      return { lines: [['Federal aid', money(r.rev_fed)], ['Share of total revenue', r.fed_share.toFixed(1) + '%']], note: 'Source: DOE-25 District Profile. The DOE-25 also reports $473,496 of operating spending paid from CARES Act funds in FY 2020-21.' };
    }
  };
  ROWS.sgp = {
    aria: 'Mean student growth percentile in reading and math, by fiscal year',
    domain: [40, 70], ticks: [40, 50, 60], axis: false, noTestMark: true,
    tickFmt: function (v) { return v; },
    series: [
      { id: 'typ', get: function (r) { return r.sgp_rea != null ? 50 : null; }, comp: true },
      { id: 'mat', get: function (r) { return r.sgp_mat; }, alt: 'square' },
      { id: 'rea', get: function (r) { return r.sgp_rea; }, main: true }
    ],
    label: function (r) {
      if (r.sgp_rea == null) return { big: '—', sub: r.no_test ? 'No statewide results for 2019-20' : 'Growth not reported for this year', delta: '', tag: r.no_test ? 'No test' : 'Not reported', prov: true, src: 'years', field: 'sgp_rea' };
      return { big: String(r.sgp_rea), sub: 'Reading growth (mean SGP); math ' + r.sgp_mat, delta: '50 is typical statewide growth', tag: 'Actual', prov: false, src: 'years', field: 'sgp_rea' };
    },
    tip: function (r) {
      if (r.sgp_rea == null) return { lines: [['Mean growth', r.no_test ? 'not tested' : 'not reported']], note: r.no_test ? 'No statewide results were published for 2019-20.' : 'No growth figure was found in the DOE file for this year.' };
      return { lines: [['Reading', String(r.sgp_rea)], ['Math', String(r.sgp_mat)], ['Typical (statewide)', '50']], note: 'Mean student growth percentile: how much students improved compared with peers who started at a similar level. Source: NH DOE assessment files.' };
    }
  };
  ROWS.grp = {
    aria: 'Reading proficiency for students with IEPs and economically disadvantaged students, by fiscal year',
    domain: [15, 85], ticks: [20, 40, 60, 80], axis: false, noTestMark: true,
    tickFmt: function (v) { return v + '%'; },
    series: [
      { id: 'all', get: function (r) { return r.ela; }, comp: true },
      { id: 'ses', get: function (r) { return r.ela_ses; }, alt: 'square' },
      { id: 'iep', get: function (r) { return r.ela_iep; }, main: true }
    ],
    label: function (r) {
      if (r.ela_iep == null) return { big: '—', sub: r.no_test ? 'No statewide results for 2019-20' : 'Results not yet available', delta: '', tag: r.no_test ? 'No test' : 'Provisional', prov: true, src: 'years', field: 'ela_iep' };
      return { big: r.ela_iep + '%', sub: 'Students with IEPs proficient in reading', delta: 'Economically disadvantaged: ' + r.ela_ses + '%', tag: 'Actual', prov: false, src: 'years', field: 'ela_iep' };
    },
    tip: function (r) {
      if (r.ela_iep == null) return { lines: [['Reading', r.no_test ? 'not tested' : 'not yet available']], note: r.no_test ? 'No statewide results were published for 2019-20.' : '' };
      return { lines: [['Students with IEPs', r.ela_iep + '%'], ['Economically disadvantaged', r.ela_ses + '%'], ['All students', r.ela + '%']], note: 'Subgroups are small, so a few students can move a year by several points. Source: NH DOE assessment files.' };
    }
  };
  ROWS.att = {
    aria: 'School attendance rate, Oyster River and New Hampshire',
    domain: [89, 99], ticks: [90, 93, 96], axis: true,
    tickFmt: function (v) { return v + '%'; },
    series: [
      { id: 'state', get: function (r) { return r.att_state; }, comp: true },
      { id: 'att', get: function (r) { return r.att; }, main: true }
    ],
    label: function (r) {
      if (r.att == null) return { big: '—', sub: r.fy > '2021-22' ? 'Published only in the DOE report viewer, which was down' : 'No attendance file for this year', delta: '', tag: 'No data', prov: true, src: 'years', field: 'att' };
      return { big: r.att + '%', sub: 'Attendance rate, all grades', delta: 'State ' + r.att_state + '%', tag: 'Actual', prov: false, src: 'years', field: 'att' };
    },
    tip: function (r) {
      if (r.att == null) return { lines: [['Attendance rate', 'not yet available']], note: 'The DOE posted district files through 2021-22; later years are in iPlatform.' };
      return { lines: [['Oyster River', r.att + '%'], ['New Hampshire', r.att_state + '%']], note: 'Share of half-days attended. Source: NH DOE attendance rate by district.' };
    }
  };
  ROWS.rate = {
    aria: 'Local school tax rate per $1,000 of assessed value in Durham, Lee and Madbury, by fiscal year',
    domain: [9, 21], ticks: [10, 15, 20], axis: false,
    tickFmt: function (v) { return '$' + v; },
    series: [
      { id: 'mad', get: function (r) { return r.tax_mad; }, comp: true },
      { id: 'lee', get: function (r) { return r.tax_lee; }, alt: 'square' },
      { id: 'dur', get: function (r) { return r.tax_dur; }, main: true }
    ],
    label: function (r) {
      if (r.tax_dur == null) return { big: '—', sub: 'Rates not yet set', delta: '', tag: 'Pending', prov: true, src: 'years', field: 'tax_dur' };
      var lee = r.tax_lee != null ? '$' + r.tax_lee.toFixed(2) : 'not yet set';
      return { big: '$' + r.tax_dur.toFixed(2), sub: 'Local school tax rate per $1,000, Durham', delta: 'Lee ' + lee + ' · Madbury $' + r.tax_mad.toFixed(2), tag: r.tax_lee == null ? 'Partial' : 'Actual', prov: r.tax_lee == null, src: 'years', field: 'tax_dur' };
    },
    tip: function (r) {
      if (r.tax_dur == null) return { lines: [['Local school rate', 'not yet set']], note: 'Set by the Department of Revenue Administration in the fall.' };
      function ln(name, loc, tot) { return [name, loc == null ? 'not yet set' : '$' + loc.toFixed(2) + ' (total $' + tot.toFixed(2) + ')']; }
      return {
        lines: [ln('Durham', r.tax_dur, r.tt_dur), ln('Lee', r.tax_lee, r.tt_lee), ln('Madbury', r.tax_mad, r.tt_mad)],
        note: 'Local education rate per $1,000 of assessed value, tax year ' + (parseInt(r.fy, 10)) + '. Rates move with each town’s revaluations as well as with spending. Sources: NH DOE valuation and tax rate files (tax years 2017 to 2025), NH Department of Revenue Administration.'
      };
    }
  };

  ROWS.share = {
    aria: 'Each town’s share of the Oyster River school property tax levy: Durham, Lee and Madbury, by fiscal year',
    domain: [8, 62], ticks: [20, 40, 60], axis: false,
    tickFmt: function (v) { return v + '%'; },
    series: [
      { id: 'mad', get: function (r) { return r.lsh_mad; }, comp: true },
      { id: 'lee', get: function (r) { return r.lsh_lee; }, alt: 'square' },
      { id: 'dur', get: function (r) { return r.lsh_dur; }, main: true }
    ],
    label: function (r) {
      if (r.lsh_dur == null) return { big: '—', sub: 'Tax year not yet filed with the DOE', delta: '', tag: 'Pending', prov: true, src: 'years', field: 'levy_dur' };
      return { big: r.lsh_dur.toFixed(0) + '%', sub: 'Durham’s share of the school property tax levy', delta: 'Lee ' + r.lsh_lee.toFixed(0) + '% · Madbury ' + r.lsh_mad.toFixed(0) + '%', tag: 'Actual', prov: false, src: 'years', field: 'levy_dur' };
    },
    tip: function (r) {
      if (r.lsh_dur == null) return { lines: [['School levy by town', 'not yet filed']], note: 'Appears when the DOE posts the tax year.' };
      function ln(nm, lv, ls, vs) { return [nm, moneyM(lv, 2) + ' · ' + ls.toFixed(1) + '% of levy (' + vs.toFixed(1) + '% of value)']; }
      return {
        lines: [ln('Durham', r.levy_dur, r.lsh_dur, r.vsh_dur), ln('Lee', r.levy_lee, r.lsh_lee, r.vsh_lee), ln('Madbury', r.levy_mad, r.lsh_mad, r.vsh_mad), ['Total school levy', moneyM(r.levy_tot, 2)]],
        note: 'Local education property tax assessed for schools, tax year ' + parseInt(r.fy, 10) + ', nominal dollars. The percentage in brackets is the town’s share of the district’s equalized property value. Source: NH DOE valuation and tax rate files.'
      };
    }
  };
  ROWS.base = {
    aria: 'Equalized property value behind each Oyster River student, by fiscal year',
    domain: [0.7e6, 2.2e6], ticks: [1e6, 1.5e6, 2e6], axis: false,
    tickFmt: function (v) { return '$' + (v / 1e6) + 'M'; },
    series: [
      { id: 'pps', get: function (r) { return r.eq_pps; }, main: true }
    ],
    label: function (r) {
      if (r.eq_pps == null) return { big: '—', sub: 'Tax year not yet filed with the DOE', delta: '', tag: 'Pending', prov: true, src: 'years', field: 'eq_tot' };
      return { big: '$' + (r.eq_pps / 1e6).toFixed(2) + 'M', sub: 'Property value behind each student', delta: '$' + (r.eq_tot / 1e9).toFixed(2) + 'B total · school levy $' + r.eff_rate.toFixed(2) + ' per $1,000', tag: 'Actual', prov: false, src: 'years', field: 'eq_tot' };
    },
    tip: function (r) {
      if (r.eq_pps == null) return { lines: [['Property value', 'not yet filed']], note: 'Appears when the DOE posts the tax year.' };
      return {
        lines: [['Equalized value, three towns', '$' + (r.eq_tot / 1e9).toFixed(2) + 'B'], ['Durham', '$' + (r.eq_dur / 1e9).toFixed(2) + 'B'], ['Lee', '$' + (r.eq_lee / 1e9).toFixed(2) + 'B'], ['Madbury', '$' + (r.eq_mad / 1e9).toFixed(2) + 'B'], ['Per student', '$' + Math.round(r.eq_pps).toLocaleString('en-US')], ['School levy per $1,000 of value', '$' + r.eff_rate.toFixed(2)]],
        note: 'Equalized value (with utilities) is the state’s estimate of full market value, tax year ' + parseInt(r.fy, 10) + ', nominal dollars. Divided by October 1 enrollment. Source: NH DOE valuation and tax rate files.'
      };
    }
  };

  var TW = [['Durham', 'dur'], ['Lee', 'lee'], ['Madbury', 'mad']];
  function appTag(r) { return r.app_basis === 'official' ? ['Actual', false] : (r.app_basis === 'derived' ? ['Computed', false] : ['Estimate', true]); }
  function townSeries(field) {
    return [
      { id: 'mad', get: function (r) { return r[field + '_mad']; }, comp: true },
      { id: 'dur', get: function (r) { return r[field + '_dur']; }, alt: 'square' },
      { id: 'lee', get: function (r) { return r[field + '_lee']; }, main: true }
    ];
  }
  function townDelta(r, field, fmt) { return 'Durham ' + fmt(r[field + '_dur']) + ' · Madbury ' + fmt(r[field + '_mad']); }
  function d2(v) { return '$' + v.toFixed(2); }
  function pc1(v) { return v.toFixed(1) + '%'; }

  ROWS.app = {
    aria: 'Share of the Oyster River school budget the apportionment formula assigns to Durham, Lee and Madbury, by fiscal year',
    domain: [10, 58], ticks: [20, 40, 55], axis: false,
    tickFmt: function (v) { return v + '%'; },
    series: [
      { id: 'mad', get: function (r) { return r.app_mad; }, comp: true },
      { id: 'dur', get: function (r) { return r.app_dur; }, alt: 'square' },
      { id: 'lee', get: function (r) { return r.app_lee; }, main: true, prov: function (r) { return r.app_basis === 'estimate'; } }
    ],
    label: function (r) {
      var tg = appTag(r);
      return { big: pc1(r.app_lee), sub: 'Lee’s share of the school budget under the 50/50 formula', delta: townDelta(r, 'app', pc1), tag: tg[0], prov: tg[1], src: 'years', field: 'app_lee' };
    },
    tip: function (r) {
      function ln(nm, t) { return [nm, pc1(r['app_' + t]) + ' of budget · ' + pc1(r['af_' + t]) + ' of students · ' + pc1(r['vf_' + t]) + ' of value']; }
      var how = r.app_basis === 'official' ? (r.fy >= '2021-22' ? 'Percentages computed from the town amounts on the NH DOE cooperative apportionment sheet published by the Department of Revenue Administration.' : 'Percentages as printed in the ORCSD annual report.') : (r.app_basis === 'derived' ? 'Computed here from the DOE levy and state credits, because the annual report no longer prints the split. The same method gives the official FY 2023-24 figure to 0.001 point.' : 'Estimate from the latest DOE files. The split approved on October 30, 2026 was not in the board materials found.');
      return {
        lines: [ln('Durham', 'dur'), ln('Lee', 'lee'), ln('Madbury', 'mad')],
        note: 'Half of the operating budget is divided by each town’s share of students (average daily membership) and half by its share of equalized property value, using the DOE file for ' + r.adm_file + ' (the latest available when the budget is set). ' + how + ' State aid is credited to each town afterwards, so what a town actually pays differs from these shares. Source: NH DOE apportionment formulas and equalized valuation per pupil files; ORCSD annual reports.'
      };
    }
  };
  ROWS.eff = {
    aria: 'School property tax per $1,000 of equalized property value in Durham, Lee and Madbury, by fiscal year',
    domain: [7, 19], ticks: [8, 12, 16], axis: false,
    tickFmt: function (v) { return '$' + v; },
    series: townSeries('eff'),
    label: function (r) {
      if (r.eff_lee == null) return nodata('Tax year not yet filed with the DOE', 'levy_lee', 'years', 'Pending');
      return { big: d2(r.eff_lee), sub: 'Lee’s school tax per $1,000 of full property value', delta: townDelta(r, 'eff', d2), tag: 'Actual', prov: false, src: 'derived', field: 'eff_lee' };
    },
    tip: function (r) {
      if (r.eff_lee == null) return { lines: [['School tax per $1,000 of value', 'not yet filed']], note: 'Appears when the DOE posts the tax year.' };
      function ln(nm, t) { return [nm, d2(r['eff_' + t]) + ' · levy ' + moneyM(r['levy_' + t], 2)]; }
      return {
        lines: [ln('Durham', 'dur'), ln('Lee', 'lee'), ln('Madbury', 'mad')],
        note: 'Net school levy divided by equalized value with utilities, tax year ' + parseInt(r.fy, 10) + '. Equalized value is the state’s estimate of full market value, so this compares what each town pays for the same dollar of property regardless of when it last revalued. Source: NH DOE valuation and tax rate files.'
      };
    }
  };
  ROWS.sch = {
    aria: 'Share of each town’s total property tax rate that goes to schools, local plus state education tax, by fiscal year',
    domain: [55, 80], ticks: [60, 70, 80], axis: false,
    tickFmt: function (v) { return v + '%'; },
    series: townSeries('sch'),
    label: function (r) {
      if (r.sch_lee == null) return nodata('Tax year not yet set for all three towns', 'sch_lee', 'derived', 'Pending');
      return { big: pc1(r.sch_lee), sub: 'Share of Lee’s total tax rate that pays for schools', delta: townDelta(r, 'sch', pc1), tag: 'Actual', prov: false, src: 'derived', field: 'sch_lee' };
    },
    tip: function (r) {
      if (r.sch_lee == null) return { lines: [['School share of tax rate', 'not yet set']], note: 'Appears when the tax rates for the year are set.' };
      function ln(nm, t) { return [nm, pc1(r['sch_' + t]) + ' · school $' + (r['tax_' + t] + r['ssr_' + t]).toFixed(2) + ' (local $' + r['tax_' + t].toFixed(2) + ' + state $' + r['ssr_' + t].toFixed(2) + ') of $' + r['tt_' + t].toFixed(2)]; }
      return {
        lines: [ln('Durham', 'dur'), ln('Lee', 'lee'), ln('Madbury', 'mad')],
        note: 'Local school rate plus the state education rate, as a share of the total rate per $1,000 (town, county, local school and state school), tax year ' + parseInt(r.fy, 10) + '. Rates are on assessed value and move with revaluations. Sources: NH DOE and Department of Revenue Administration rates; state education rates from the ORCSD annual reports.'
      };
    }
  };
  ROWS.cred = {
    aria: 'Share of each town’s formula share of the school budget that state aid credits cover, by fiscal year',
    domain: [10, 33], ticks: [15, 20, 30], axis: false,
    tickFmt: function (v) { return v + '%'; },
    series: townSeries('crs'),
    label: function (r) {
      if (r.crs_lee == null) return nodata('Tax year not yet filed with the DOE', 'cr_lee', 'years', 'Pending');
      return { big: pc1(r.crs_lee), sub: 'Share of Lee’s formula share covered by state aid', delta: townDelta(r, 'crs', pc1), tag: 'Actual', prov: false, src: 'derived', field: 'crs_lee' };
    },
    tip: function (r) {
      if (r.crs_lee == null) return { lines: [['State credit', 'not yet filed']], note: 'Appears when the DOE posts the tax year.' };
      function ln(nm, t) { return [nm, pc1(r['crs_' + t]) + ' · credit ' + moneyM(r['cr_' + t], 2) + ' of ' + moneyM(r['cr_' + t] + r['levy_' + t], 2)]; }
      return {
        lines: [ln('Durham', 'dur'), ln('Lee', 'lee'), ln('Madbury', 'mad')],
        note: 'Each town’s formula share is reduced by its own adequacy grant and the state education property tax it keeps; what is left is its school levy. Because the credits follow each town’s own students and property wealth, they cover more of Lee’s and Madbury’s share than Durham’s. Source: NH DOE adequate education aid municipal summaries; ORCSD annual reports.'
      };
    }
  };
  ROWS.pps3 = {
    money: true,
    aria: 'Net school property tax levy per resident student in Durham, Lee and Madbury, by fiscal year',
    domain: [10000, 28000], ticks: [12000, 18000, 24000], axis: false,
    tickFmt: function (v) { return '$' + (v / 1000) + 'K'; },
    series: townSeries('pps'),
    label: function (r) {
      if (r.pps_lee == null) return nodata('Tax year not yet filed with the DOE', 'levy_lee', 'years', 'Pending');
      return { big: money(r.pps_lee), sub: 'Lee’s school levy per resident student', delta: townDelta(r, 'pps', money), tag: 'Actual', prov: false, src: 'derived', field: 'pps_lee' };
    },
    tip: function (r) {
      if (r.pps_lee == null) return { lines: [['Levy per resident student', 'not yet filed']], note: 'Appears when the DOE posts the tax year.' };
      function ln(nm, t) { return [nm, money(r['pps_' + t]) + ' · ' + num(r['adm_' + t]) + ' students']; }
      return {
        lines: [ln('Durham', 'dur'), ln('Lee', 'lee'), ln('Madbury', 'mad')],
        note: 'Net school levy divided by the town’s average daily membership in residence, from the DOE file for ' + r.adm_file + ' that the formula used. Durham’s higher figure reflects its larger property base. Source: NH DOE valuation and equalized valuation per pupil files.'
      };
    }
  };
  ROWS.app.chg = { get: function (r) { return r.app_lee; }, kind: 'pts', dec: true, note: 'Lee' };
  ROWS.eff.chg = { get: function (r) { return r.eff_lee; }, kind: 'pct', note: 'Lee' };
  ROWS.sch.chg = { get: function (r) { return r.sch_lee; }, kind: 'pts', dec: true, note: 'Lee' };
  ROWS.cred.chg = { get: function (r) { return r.crs_lee; }, kind: 'pts', dec: true, note: 'Lee' };
  ROWS.pps3.chg = { get: function (r) { return r.pps_lee; }, kind: 'pct', note: 'Lee' };

  // ---- Added Nov 22, 2026: state building aid, special education aid, and the DOE school safety data ----
  ROWS.bldaid = {
    money: true,
    aria: 'State building aid paid to Oyster River for school construction bonds, by fiscal year',
    domain: [0, 600000], ticks: [0, 200000, 400000, 600000], axis: false,
    tickFmt: function (v) { return v === 0 ? '$0' : '$' + (v / 1000) + 'K'; },
    series: [{ id: 'bld', get: function (r) { return r.bld_aid; }, main: true }],
    label: function (r) {
      if (r.bld_aid == null) return nodata('Not in the state schedule', 'bld_aid', 'years');
      return { big: r.bld_aid === 0 ? '$0' : money(r.bld_aid), sub: 'State building aid for school bonds', delta: r.bld_aid === 0 ? 'Ended after 2022-23' : '', tag: r.fy > '2025-26' ? 'Scheduled' : 'Actual', prov: r.fy > '2025-26', src: 'years', field: 'bld_aid' };
    },
    tip: function (r) {
      if (r.bld_aid == null) return { lines: [['Building aid', 'not in the schedule']], note: '' };
      return { lines: [['State building aid', money(r.bld_aid)]], note: 'Paid by the NH DOE toward the principal and interest on approved school construction bonds. Oyster River received $687,618 in 2009-10, $678,618 in 2010-11, $552,618 in 2011-12 and $523,742 a year from 2012-13 through 2022-23; the state schedule shows $0 from 2023-24 on, including 2026-27 through 2040-41. Each dollar of aid that ends is replaced by local property taxes unless bond payments fall by the same amount. Source: NH DOE Building Aid Distribution, last revised June 30, 2026.' };
    }
  };
  ROWS.bldaid.chg = { get: function (r) { return r.bld_aid; }, kind: 'pct', note: 'building aid' };
  ROWS.spedaid = {
    money: true,
    aria: 'State special education aid and the district cost of the high-cost students it covers, by fiscal year',
    domain: [0, 950000], ticks: [0, 250000, 500000, 750000], axis: false,
    tickFmt: function (v) { return v === 0 ? '$0' : '$' + (v / 1000) + 'K'; },
    series: [
      { id: 'spc', get: function (r) { return r.sp_cost; }, alt: 'square' },
      { id: 'spe', get: function (r) { return r.sp_ent; }, main: true }
    ],
    label: function (r) {
      if (r.sp_ent == null) return nodata('Not yet published by the NH DOE', 'sp_ent', 'years', 'Pending');
      return { big: money(r.sp_ent), sub: 'State special education aid owed to the district', delta: 'High-cost student costs ' + money(r.sp_cost), tag: 'Actual', prov: false, src: 'years', field: 'sp_ent' };
    },
    tip: function (r) {
      if (r.sp_ent == null) return { lines: [['Special education aid', 'not yet published']], note: '' };
      var L = [['Aid owed (entitlement)', money(r.sp_ent)]];
      if (r.sp_paid != null) L.push(['Aid paid after proration', money(r.sp_paid)]);
      L.push(['District cost of eligible students', money(r.sp_cost)]);
      if (r.cte_tt != null) L.push(['Career technology transportation aid', money(r.cte_tt)]);
      if (r.efa_po != null) L.push(['EFA phase-out grant to the district', money(r.efa_po)]);
      return { lines: L, note: 'The DOE pays part of the cost of educating students whose special education costs exceed 3.5 times the state average cost per pupil, and the state appropriation is sometimes prorated. Each fiscal year’s aid is based on the previous school year’s costs. The 2020-21 and 2021-22 files list only the entitlement. The transportation aid is for students attending career technology centers and is listed by school year. The phase-out grant is the DOE’s payment to districts that lose adequacy aid because of Education Freedom Accounts; the 2023-24 amount could not be read. Source: NH DOE other state aid programs.' };
    }
  };
  ROWS.spedaid.chg = { get: function (r) { return r.sp_ent; }, kind: 'pct', note: 'aid owed' };
  ROWS.grad = {
    aria: 'Oyster River four-year high school graduation rate, by fiscal year',
    domain: [90, 100], ticks: [92, 96, 100], axis: false,
    tickFmt: function (v) { return v + '%'; },
    series: [{ id: 'g4', get: function (r) { return r.grad4; }, main: true }],
    label: function (r) {
      if (r.grad4 == null) return nodata(r.fy < '2021-22' ? 'The DOE dashboard starts at 2021-22' : 'Not yet reported', 'grad4');
      return { big: p1(r.grad4), sub: 'Of the class graduated in four years', delta: r.grad5 == null ? '' : 'Five-year ' + p1(r.grad5), tag: 'Actual', prov: false, src: 'years', field: 'grad4' };
    },
    tip: function (r) {
      if (r.grad4 == null) return { lines: [['Graduation rate', 'not available']], note: 'The DOE iExplore dashboard shows the last five years. Earlier rates are in the DOE cohort reports.' };
      var L = [['Four-year rate', p1(r.grad4)], ['Five-year rate', r.grad5 == null ? 'not reported' : p1(r.grad5)]];
      if (r.psenr != null) L.push(['Enrolled in college within a year', p1(r.psenr)]);
      return { lines: L, note: 'Share of the graduating cohort that finished in four (or five) years, with the year labeled as the DOE labels it. No New Hampshire figure is shown: the state value on the DOE dashboard is not a graduation rate. Source: NH DOE iExplore.' };
    }
  };
  ROWS.part = {
    aria: 'Share of Oyster River students who took the state English language arts test, by fiscal year',
    domain: [84, 100], ticks: [88, 92, 96], axis: false,
    tickFmt: function (v) { return v + '%'; },
    series: [{ id: 'pe', get: function (r) { return r.pt_ela; }, main: true }],
    label: function (r) {
      if (r.pt_ela == null) return nodata(r.fy === '2019-20' ? 'No state test in spring 2020' : 'Not yet reported', 'pt_ela');
      return { big: r.pt_ela + '%', sub: 'Students tested in reading and writing', delta: 'Science ' + r.pt_sci + '%', tag: 'Actual', prov: false, src: 'years', field: 'pt_ela' };
    },
    tip: function (r) {
      if (r.pt_ela == null) return { lines: [['Participation', r.fy === '2019-20' ? 'no test (COVID-19)' : 'not yet reported']], note: 'The state did not give its tests in spring 2020.' };
      return { lines: [['Reading and writing', r.pt_ela + '%'], ['Math', r.pt_mat + '%'], ['Science', r.pt_sci + '%']], note: 'Share of students required to test who did. Science is given in grades 5, 8 and 11 only. Federal rules call for 95%. Source: NH DOE iAchieve (assessment participation).' };
    }
  };
  ROWS.trunt = {
    aria: 'Oyster River students counted as habitually truant, by fiscal year',
    domain: [0, 190], ticks: [0, 50, 100, 150], axis: false,
    tickFmt: function (v) { return String(v); },
    series: [{ id: 'tr', get: function (r) { return r.truant; }, main: true }],
    label: function (r) {
      if (r.truant == null) return nodata(r.fy > '2024-25' ? 'Not yet published by the NH DOE' : 'No report', 'truant', 'years', 'Pending');
      var per = r.enrollment ? ' · ' + (r.truant / r.enrollment * 100).toFixed(1) + ' per 100 students' : '';
      return { big: String(r.truant), sub: 'Students habitually truant' + per, delta: '', tag: 'Actual', prov: false, src: 'years', field: 'truant' };
    },
    tip: function (r) {
      if (r.truant == null) return { lines: [['Habitually truant students', 'not yet published']], note: '' };
      return { lines: [['Students habitually truant', String(r.truant)], ['Per 100 students enrolled', r.enrollment ? (r.truant / r.enrollment * 100).toFixed(1) : '—']], note: 'Habitually truant means ten half days of unexcused absence during the school year. The district reports this to the DOE, and counts depend on how each school records excused and unexcused absences, so changes between years can reflect practice as well as behavior: in 2020-21 the middle school reported 149 of the 165 and in 2024-25 the high school reported 67 of the 105. Source: NH School Safety Data Collection, Section 6.' };
    }
  };
  ROWS.grad.chg = { get: function (r) { return r.grad4; }, kind: 'pts', dec: true, note: 'four-year rate' };
  ROWS.part.chg = { get: function (r) { return r.pt_ela; }, kind: 'pts', note: 'reading and writing' };
  ROWS.trunt.chg = { get: function (r) { return r.truant; }, kind: 'pts', unit: 'students', note: 'habitually truant' };
  ROWS.susp = {
    aria: 'Students who received out-of-school and in-school suspensions, by fiscal year',
    domain: [0, 70], ticks: [0, 20, 40, 60], axis: false,
    tickFmt: function (v) { return String(v); },
    series: [
      { id: 'iss', get: function (r) { return r.iss; }, alt: 'square' },
      { id: 'oss', get: function (r) { return r.oss; }, main: true }
    ],
    label: function (r) {
      if (r.oss == null) return nodata(r.fy > '2024-25' ? 'Not yet published by the NH DOE' : 'No report', 'oss', 'years', 'Pending');
      return { big: String(r.oss), sub: 'Students with an out-of-school suspension', delta: 'In-school suspensions ' + r.iss + ' · expelled ' + r.expel, tag: 'Actual', prov: false, src: 'years', field: 'oss' };
    },
    tip: function (r) {
      if (r.oss == null) return { lines: [['Suspensions', 'not yet published']], note: '' };
      return { lines: [['Students with out-of-school suspension', String(r.oss)], ['Students with in-school suspension', String(r.iss)], ['Students expelled', String(r.expel)], ['Out-of-school per 100 students', r.enrollment ? (r.oss / r.enrollment * 100).toFixed(1) : '—']], note: 'Counts of students, not suspensions, from the district’s School Safety Data Collection report (Section 4). A student suspended in school and out of school may be counted in both lines. Source: NH DOE school safety data.' };
    }
  };
  ROWS.susp.chg = { get: function (r) { return r.oss; }, kind: 'pts', unit: 'students', note: 'out-of-school suspensions' };
  ROWS.bully = {
    aria: 'Reported and investigated bullying incidents in Oyster River schools, by fiscal year',
    domain: [0, 16], ticks: [0, 5, 10, 15], axis: false,
    tickFmt: function (v) { return String(v); },
    series: [
      { id: 'bc', get: function (r) { return r.bul_act; }, alt: 'square' },
      { id: 'br', get: function (r) { return r.bul_rep; }, main: true }
    ],
    label: function (r) {
      if (r.bul_rep == null) return nodata(r.fy > '2024-25' ? 'Not yet published by the NH DOE' : 'No report', 'bul_rep', 'years', 'Pending');
      return { big: String(r.bul_rep), sub: 'Bullying incidents reported', delta: 'Investigated and confirmed ' + r.bul_act, tag: 'Actual', prov: false, src: 'years', field: 'bul_rep' };
    },
    tip: function (r) {
      if (r.bul_rep == null) return { lines: [['Bullying', 'not yet published']], note: '' };
      return { lines: [['Reported incidents of bullying', String(r.bul_rep)], ['Reported cyber-bullying', String(r.bul_cyb)], ['Investigated and confirmed bullying', String(r.bul_act)], ['Investigated and confirmed cyber-bullying', String(r.bul_acy)]], note: 'Reports under the state bullying law (RSA 193-F), as the district submitted them. Counts are small, and the very low 2018-19 to 2020-21 figures may reflect how reports were recorded as well as how many occurred. Source: NH School Safety Data Collection, Section 3.' };
    }
  };
  ROWS.bully.chg = { get: function (r) { return r.bul_rep; }, kind: 'pts', unit: 'reports', note: 'reported incidents' };
  ROWS.viol = {
    aria: 'Violence, weapons, drug and alcohol incidents in Oyster River schools, by fiscal year',
    domain: [0, 48], ticks: [0, 10, 20, 30, 40], axis: false,
    tickFmt: function (v) { return String(v); },
    series: [{ id: 'vi', get: function (r) { return r.inc_ser; }, main: true }],
    label: function (r) {
      if (r.inc_ser == null) return nodata(r.fy > '2024-25' ? 'Not yet published by the NH DOE' : 'No report', 'inc_ser', 'derived', 'Pending');
      return { big: String(r.inc_ser), sub: 'Violence, weapons, drug and alcohol incidents', delta: 'Drugs ' + r.drug + ' · violence ' + (r.vio_inj + r.vio_non) + ' · alcohol ' + r.alc + ' · weapons ' + r.weap, tag: 'Actual', prov: false, src: 'derived', field: 'inc_ser' };
    },
    tip: function (r) {
      if (r.inc_ser == null) return { lines: [['Incidents', 'not yet published']], note: '' };
      return { lines: [['Violence with injury needing medical care', String(r.vio_inj)], ['Violence without injury (incl. harassment, bullying)', String(r.vio_non)], ['Weapons possession', String(r.weap)], ['Illicit drugs', String(r.drug)], ['Alcohol', String(r.alc)], ['Other drug, alcohol, violence or weapons', String(r.vio_oth)], ['Total', String(r.inc_ser)]], note: 'Incidents in the Student Discipline section of the DOE School Safety Data Collection (Section 4) that the district reported. The 34 drug incidents in 2017-18 are the largest single category in the series. Counts are small enough that one event or a change in how incidents are coded can move a year. Section 5 (homicides, firearms, arson and other serious crimes) is zero in every year. Source: NH DOE school safety data.' };
    }
  };
  ROWS.viol.chg = { get: function (r) { return r.inc_ser; }, kind: 'pts', unit: 'incidents', note: 'reported incidents' };
  ROWS.vote = {
    aria: 'Share of voters approving the Oyster River operating budget, by fiscal year',
    domain: [50, 100], ticks: [60, 70, 80, 90], axis: false,
    tickFmt: function (v) { return v + '%'; },
    series: [{ id: 'vt', get: function (r) { return r.vote_y == null ? null : 100 * r.vote_y / (r.vote_y + r.vote_n); }, main: true }],
    label: function (r) {
      if (r.vote_y == null) return nodata('No vote result', 'vote_y', 'years');
      var p = 100 * r.vote_y / (r.vote_y + r.vote_n);
      return { big: p.toFixed(0) + '%', sub: 'Yes votes on the operating budget', delta: 'Yes ' + r.vote_y.toLocaleString('en-US') + ' · No ' + r.vote_n.toLocaleString('en-US'), tag: 'Actual', prov: false, src: 'years', field: 'vote_y' };
    },
    tip: function (r) {
      if (r.vote_y == null) return { lines: [['Budget vote', 'no result']], note: '' };
      var p = 100 * r.vote_y / (r.vote_y + r.vote_n);
      return { lines: [['Yes', r.vote_y.toLocaleString('en-US')], ['No', r.vote_n.toLocaleString('en-US')], ['Yes share', p.toFixed(1) + '%'], ['Total ballots on the article', (r.vote_y + r.vote_n).toLocaleString('en-US')]], note: 'Ballot result on the operating budget article (a simple majority passes it) in the March election that sets the fiscal year shown, for example March 2026 for 2026-27. Results come from the district annual report for that year, or the district’s official March 10, 2026 results for 2026-27. Turnout swings with what else is on the ballot, so compare years with care.' };
    }
  };
  ROWS.vote.chg = { get: function (r) { return r.vote_y == null ? null : 100 * r.vote_y / (r.vote_y + r.vote_n); }, kind: 'pts', dec: 0, unit: 'points', note: 'yes share' };
  ROWS.restr = {
    aria: 'Physical restraint and seclusion reports in Oyster River schools, by fiscal year',
    domain: [0, 40], ticks: [0, 10, 20, 30], axis: false,
    tickFmt: function (v) { return String(v); },
    series: [
      { id: 'sec', get: function (r) { return r.seclu; }, alt: 'square' },
      { id: 'res', get: function (r) { return r.restr; }, main: true }
    ],
    label: function (r) {
      if (r.restr == null) return nodata(r.fy > '2024-25' ? 'Not yet published by the NH DOE' : 'No report', 'restr', 'years', 'Pending');
      return { big: String(r.restr + r.seclu), sub: 'Restraint and seclusion reports', delta: 'Restraints ' + r.restr + ' · seclusions ' + r.seclu, tag: 'Actual', prov: false, src: 'years', field: 'restr' };
    },
    tip: function (r) {
      if (r.restr == null) return { lines: [['Restraints and seclusions', 'not yet published']], note: '' };
      return { lines: [['Physical restraint reports', String(r.restr)], ['Seclusion reports', String(r.seclu)]], note: 'Reports of physical restraint and seclusion filed under the state rules (Section 1 of the School Safety Data Collection). The district reported none from 2015-16 through 2021-22; the counts since then are small and should not be read as a trend. Source: NH DOE school safety data.' };
    }
  };
  ROWS.restr.chg = { get: function (r) { return r.restr == null ? null : r.restr + r.seclu; }, kind: 'pts', unit: 'reports', note: 'restraints and seclusions' };
  ROWS.tstart = {
    money: true,
    aria: 'Minimum starting salary for a teacher with a bachelor’s degree, Oyster River and the New Hampshire average, by fiscal year',
    domain: [34000, 56000], ticks: [38000, 44000, 50000], axis: false,
    tickFmt: function (v) { return '$' + (v / 1000) + 'K'; },
    series: [
      { id: 'nh', get: function (r) { return r.t_start_state; }, comp: true },
      { id: 'orc', get: function (r) { return r.t_start; }, main: true }
    ],
    label: function (r) {
      if (r.t_start == null) return { big: '—', sub: 'Not yet published by the NH DOE', delta: '', tag: 'Pending', prov: true, src: 'years', field: 't_start' };
      var d = r.t_start_state != null ? 'NH average ' + money(r.t_start_state) + ' · ' + signPct((r.t_start / r.t_start_state - 1) * 100) : 'NH average not published for this year';
      return { big: money(r.t_start), sub: 'Starting salary, bachelor’s degree, no experience', delta: d, tag: 'Actual', prov: false, src: 'years', field: 't_start' };
    },
    tip: function (r) {
      if (r.t_start == null) return { lines: [['Starting salary', 'not yet published']], note: 'Appears when the DOE posts the year.' };
      var L = [['Oyster River', money(r.t_start)]];
      if (r.t_start_state != null) { L.push(['NH average minimum', money(r.t_start_state)]); L.push(['Gap', signPct((r.t_start / r.t_start_state - 1) * 100)]); }
      return { lines: L, note: 'Lowest step on the district salary schedule for a bachelor’s degree. The NH figure is an unweighted average of districts that reported. Source: NH DOE teacher minimum starting salary files.' };
    }
  };
  ROWS.tavg = {
    money: true,
    aria: 'Average teacher salary, Oyster River and the New Hampshire average, by fiscal year',
    domain: [55000, 86000], ticks: [60000, 70000, 80000], axis: false,
    tickFmt: function (v) { return '$' + (v / 1000) + 'K'; },
    series: [
      { id: 'nh', get: function (r) { return r.t_avg_state; }, comp: true },
      { id: 'orc', get: function (r) { return r.t_avg; }, main: true }
    ],
    label: function (r) {
      if (r.t_avg == null && r.t_avg_note) return { big: '—', sub: r.fy === '2024-25' ? 'DOE file repeats the prior year, not plotted' : 'DOE figure looks out of line, not plotted', delta: 'NH average ' + money(r.t_avg_state), tag: 'Check', prov: true, src: 'years', field: 't_avg_file' };
      if (r.t_avg == null) return { big: '—', sub: 'Not yet published by the NH DOE', delta: '', tag: 'Pending', prov: true, src: 'years', field: 't_avg' };
      return { big: money(r.t_avg), sub: 'Average teacher salary', delta: 'NH average ' + money(r.t_avg_state) + ' · ' + signPct((r.t_avg / r.t_avg_state - 1) * 100), tag: 'Actual', prov: false, src: 'years', field: 't_avg' };
    },
    tip: function (r) {
      if (r.t_avg == null && r.t_avg_note) return { lines: [['Oyster River (DOE file, as listed)', '$' + r.t_avg_file.toLocaleString('en-US') + ' nominal'], ['NH average', money(r.t_avg_state)]], note: r.t_avg_note + ' Source: NH DOE teacher average salary files.' };
      if (r.t_avg == null) return { lines: [['Average teacher salary', 'not yet published']], note: 'Appears when the DOE posts the year.' };
      return { lines: [['Oyster River', money(r.t_avg)], ['NH average', money(r.t_avg_state)], ['Gap', signPct((r.t_avg / r.t_avg_state - 1) * 100)], ['Teachers counted', r.t_avg_fte.toFixed(1) + ' FTE']], note: 'Average salary of teachers in the district, as reported to the NH DOE, before benefits. Source: NH DOE teacher average salary files.' };
    }
  };
  ROWS.ratio = {
    aria: 'Students per teacher, Oyster River and the New Hampshire total, by fiscal year',
    domain: [10.5, 13.2], ticks: [11, 12, 13], axis: false,
    tickFmt: function (v) { return String(v); },
    series: [
      { id: 'nh', get: function (r) { return r.ratio_state; }, comp: true },
      { id: 'orc', get: function (r) { return r.ratio; }, main: true }
    ],
    label: function (r) {
      if (r.ratio == null) return { big: '—', sub: 'Not yet published by the DOE', delta: '', tag: 'No data', prov: true, src: 'years', field: 'ratio' };
      return { big: r.ratio.toFixed(1), sub: 'Students per teacher', delta: r.ratio_state != null ? 'NH ' + r.ratio_state.toFixed(1) : 'NH total not in this year’s file', tag: 'Actual', prov: false, src: 'years', field: 'ratio' };
    },
    tip: function (r) {
      if (r.ratio == null) return { lines: [['Student-teacher ratio', 'not available']], note: 'The DOE publishes the Oct 1 ratio the following winter; nothing is published yet for this year.' };
      var L = [['Oyster River', r.ratio.toFixed(1) + ' students per teacher'], ['NH total', r.ratio_state != null ? r.ratio_state.toFixed(1) : 'not in file'], ];
      if (r.ratio_teachers != null) L.push(['Teachers (FTE)', r.ratio_teachers.toFixed(1)], ['Students counted', r.ratio_enr.toLocaleString('en-US')]);
      return { lines: L, note: 'The DOE counts students and teachers its own way, so the student count differs from the October 1 enrollment elsewhere on this page. Source: NH DOE student to teacher ratio files (iPlatform for 2022-23 on).' };
    }
  };

  function nodata(msg, field, src, tag) { return { big: '—', sub: msg, delta: '', tag: tag || 'No data', prov: true, src: src || 'years', field: field }; }
  function p1(v) { return v.toFixed(1) + '%'; }
  function chgPct(f) { return function (r) { return r[f]; }; }

  ROWS.lvlenr = {
    aria: 'October 1 enrollment by school level: kindergarten to grade 4, middle school and high school, by fiscal year',
    domain: [540, 900], ticks: [600, 700, 800], axis: false,
    tickFmt: function (v) { return String(v); },
    series: [
      { id: 'k4', get: function (r) { return r.en_k4; }, comp: true },
      { id: 'ms', get: function (r) { return r.en_ms; }, alt: 'square' },
      { id: 'hs', get: function (r) { return r.en_hs; }, main: true }
    ],
    label: function (r) {
      if (r.en_hs == null) return nodata('Fall count not taken yet', 'en_hs', 'years', 'Pending');
      return { big: num(r.en_hs), sub: 'High school students (grades 9 to 12)', delta: 'Middle ' + num(r.en_ms) + ' · K to 4 ' + num(r.en_k4), tag: 'Actual', prov: false, src: 'years', field: 'en_hs' };
    },
    tip: function (r) {
      if (r.en_hs == null) return { lines: [['Enrollment by level', 'not yet counted']], note: 'The October 1 count for this year has not been taken.' };
      var L = [['High school (9-12)', num(r.en_hs)], ['Middle school (5-8)', num(r.en_ms)], ['K to grade 4', num(r.en_k4)]];
      var rest = r.enrollment - r.en_hs - r.en_ms - r.en_k4;
      if (rest > 0) L.push(['Not itemized by level', num(rest)]);
      L.push(['Total', num(r.enrollment)]);
      return { lines: L, note: 'October 1 counts. K to 4 adds kindergarten and grades 1 to 4. In 2020-21 through 2024-25 the DOE total is 25 to 30 students higher than the four levels add up to; the report does not say who they are. Source: NH DOE fall enrollment, as printed in the ORCSD 2026 annual report.' };
    }
  };
  ROWS.fb = {
    money: true,
    aria: 'General fund balance at June 30: total and unassigned, by fiscal year',
    domain: [0, 4300000], ticks: [0, 1000000, 2000000, 3000000, 4000000], axis: false,
    tickFmt: function (v) { return v === 0 ? '$0' : '$' + (v / 1e6) + 'M'; },
    series: [
      { id: 'un', get: function (r) { return r.fb_un; }, alt: 'square' },
      { id: 'tot', get: function (r) { return r.fb_tot; }, main: true }
    ],
    label: function (r) {
      if (r.fb_tot == null && r.fb_un_pre != null) return { big: moneyM(r.fb_un_pre, 2), sub: 'Unassigned balance, preliminary (audit not posted)', delta: 'Total not yet available', tag: 'Preliminary', prov: true, src: 'years', field: 'fb_un_pre' };
      if (r.fb_tot == null) return nodata('Audit for this year not yet posted', 'fb_tot', 'years', 'Pending');
      return { big: moneyM(r.fb_tot, 2), sub: 'General fund balance at June 30', delta: 'Unassigned ' + moneyM(r.fb_un, 2), tag: 'Audited', prov: false, src: 'years', field: 'fb_tot' };
    },
    tip: function (r) {
      if (r.fb_tot == null && r.fb_un_pre != null) return { lines: [['Unassigned fund balance (preliminary)', money(r.fb_un_pre)], ['Total fund balance', 'not yet posted']], note: 'From the district June 2025 monthly financial report, which is preliminary and unaudited. The FY2025 audit has not been posted. Total and committed balances will be added when it is.' };
      if (r.fb_tot == null) return { lines: [['Fund balance', 'not yet posted']], note: 'The audit for this year has not been posted. The district’s audits are on orcsd.org under Business Office.' };
      var L = [['Total general fund balance', money(r.fb_tot)], ['Unassigned (free to use)', money(r.fb_un)], ['Committed (set aside)', money(r.fb_com)]];
      if (r.actual_recurring != null) L.push(['Unassigned ÷ operating spending', p1(r.fb_un / r.actual_recurring * 100)]);
      return { lines: L, note: 'Audited general fund balances at June 30. Committed money is set aside for specific purposes such as the facilities and special education trusts and encumbrances. Unassigned balance can be used to lower the next tax rate. Source: ORCSD audited financial statements.' };
    }
  };
  ROWS.cls = {
    aria: 'Average class size in grades 1 to 4 at Mast Way and Moharimet compared with the New Hampshire average, by fiscal year',
    domain: [15, 22], ticks: [16, 18, 20], axis: false,
    tickFmt: function (v) { return String(v); },
    series: [
      { id: 'nh', get: function (r) { return r.cs_st; }, comp: true },
      { id: 'orc', get: function (r) { return r.cs_d; }, main: true }
    ],
    label: function (r) {
      if (r.cs_d == null) return nodata('The DOE has not published this year', 'cs_d', 'derived');
      return { big: r.cs_d.toFixed(1), sub: 'Students per class, grades 1 to 4', delta: 'NH ' + r.cs_st.toFixed(1), tag: 'Actual', prov: false, src: 'derived', field: 'cs_d' };
    },
    tip: function (r) {
      if (r.cs_d == null) return { lines: [['Class size', 'not yet published']], note: 'The DOE publishes class sizes (as of October 1) the following winter; nothing is published yet for this year.' };
      return { lines: [['Grades 1-2, Mast Way', r.cs_mw12.toFixed(1)], ['Grades 1-2, Moharimet', r.cs_mo12.toFixed(1)], ['Grades 3-4, Mast Way', r.cs_mw34.toFixed(1)], ['Grades 3-4, Moharimet', r.cs_mo34.toFixed(1)], ['NH grades 1-2 / 3-4', r.cs_st12.toFixed(1) + ' / ' + r.cs_st34.toFixed(1)]], note: 'Oyster River is the average of the four school and grade-band figures. The DOE lists no class size for the middle school. Source: NH DOE average class size, as printed in the ORCSD annual reports.' };
    }
  };
  ROWS.sat = {
    aria: 'Average SAT score (reading and writing plus math) at Oyster River High School compared with New Hampshire, by fiscal year',
    domain: [960, 1180], ticks: [1000, 1080, 1160], axis: false,
    tickFmt: function (v) { return String(v); },
    series: [
      { id: 'nh', get: function (r) { return r.sat_nh_tot; }, comp: true },
      { id: 'orc', get: function (r) { return r.sat_tot; }, main: true }
    ],
    label: function (r) {
      if (r.sat_tot == null) return nodata('Not yet reported', 'sat_tot', 'derived');
      return { big: String(r.sat_tot), sub: 'Average SAT, reading and writing + math', delta: 'NH ' + r.sat_nh_tot, tag: 'Actual', prov: false, src: 'derived', field: 'sat_tot' };
    },
    tip: function (r) {
      if (r.sat_tot == null) return { lines: [['SAT', 'not yet reported']], note: 'The high school counseling office reports scores after each spring test.' };
      return { lines: [['ORHS reading and writing', String(r.sat_rw)], ['ORHS math', String(r.sat_m)], ['NH reading and writing', String(r.sat_rw_nh)], ['NH math', String(r.sat_m_nh)]], note: 'Section scores run 200 to 800, so the total runs 400 to 1600. Which students test differs from year to year, so compare trends with care. National averages printed in the report are left out because the 2019 figures do not match the College Board’s. Source: ORHS counseling, as printed in the ORCSD annual reports.' };
    }
  };
  ROWS.coll = {
    aria: 'Share of Oyster River graduates entering a four-year college, compared with New Hampshire, by fiscal year',
    domain: [40, 80], ticks: [50, 60, 70], axis: false,
    tickFmt: function (v) { return v + '%'; },
    series: [
      { id: 'nh', get: function (r) { return r.col4_nh; }, comp: true },
      { id: 'orc', get: function (r) { return r.col4; }, main: true }
    ],
    label: function (r) {
      if (r.col4 == null) return nodata('Not yet reported', 'col4');
      return { big: p1(r.col4), sub: 'Graduates entering a four-year college', delta: 'NH ' + p1(r.col4_nh), tag: 'Actual', prov: false, src: 'years', field: 'col4' };
    },
    tip: function (r) {
      if (r.col4 == null) return { lines: [['After graduation', 'not yet reported']], note: 'The DOE reports plans for each graduating class about a year later.' };
      function ln(a, b) { return a.toFixed(1) + '% (NH ' + b.toFixed(1) + '%)'; }
      return { lines: [['Four-year college', ln(r.col4, r.col4_nh)], ['Other post-secondary', ln(r.coll, r.coll_nh)], ['Working', ln(r.colw, r.colw_nh)], ['Armed forces', ln(r.colm, r.colm_nh)]], note: 'Plans of all students who completed high school that year. The few who are unemployed, returning to school or unknown are left out, so the lines do not add to 100%. Source: NH DOE high school completers, as printed in the ORCSD annual reports.' };
    }
  };
  ROWS.sped = {
    aria: 'Students receiving special education services as a share of October 1 enrollment, by fiscal year',
    domain: [11, 18], ticks: [12, 14, 16], axis: false,
    tickFmt: function (v) { return v + '%'; },
    series: [{ id: 'sp', get: function (r) { return r.sp_share; }, main: true }],
    label: function (r) {
      if (r.sp_share == null) return nodata('Fall count not taken yet', 'sp_share', 'derived', 'Pending');
      return { big: p1(r.sp_share), sub: 'Students receiving special education', delta: num(r.sp_tot) + ' students', tag: 'Actual', prov: false, src: 'derived', field: 'sp_share' };
    },
    tip: function (r) {
      if (r.sp_share == null) return { lines: [['Special education', 'not yet counted']], note: '' };
      return { lines: [['Elementary', num(r.sp_el)], ['Middle school', num(r.sp_ms)], ['High school', num(r.sp_hs)], ['Out of district, ages 3-5', num(r.sp_o35)], ['Out of district, ages 6-21', num(r.sp_o621)], ['Total', num(r.sp_tot)]], note: 'Students receiving services on October 1, from the district’s special education office. The share divides by October 1 enrollment, and the total includes preschoolers and out-of-district placements, so it is an approximation.' };
    }
  };
  ROWS.frl = {
    aria: 'Students eligible for free or reduced-price lunch as a share of October 1 enrollment, by fiscal year',
    domain: [3, 11], ticks: [4, 6, 8, 10], axis: false,
    tickFmt: function (v) { return v + '%'; },
    series: [{ id: 'frl', get: function (r) { return r.frl_share; }, main: true }],
    label: function (r) {
      if (r.frl_share == null) return nodata('Not yet counted', 'frl_share', 'derived', 'Pending');
      return { big: p1(r.frl_share), sub: 'Eligible for free or reduced lunch', delta: num(r.frl) + ' students', tag: 'Actual', prov: false, src: 'derived', field: 'frl_share' };
    },
    tip: function (r) {
      if (r.frl_share == null) return { lines: [['Lunch eligibility', 'not yet counted']], note: '' };
      return { lines: [['Eligible students', num(r.frl)], ['Share of enrollment', p1(r.frl_share)]], note: 'Eligibility is based on household income. It also drives part of the state’s adequacy aid. Source: NH DOE, October 1 counts as printed in the ORCSD annual reports.' };
    }
  };
  ROWS.ell = {
    aria: 'English language learners as a share of October 1 enrollment, by fiscal year',
    domain: [1, 3], ticks: [1.5, 2, 2.5], axis: false,
    tickFmt: function (v) { return v + '%'; },
    series: [{ id: 'ell', get: function (r) { return r.ell_share; }, main: true }],
    label: function (r) {
      if (r.ell_share == null) return nodata('Not yet counted', 'ell_share', 'derived', 'Pending');
      return { big: p1(r.ell_share), sub: 'Students learning English', delta: num(r.ell) + ' students', tag: 'Actual', prov: false, src: 'derived', field: 'ell_share' };
    },
    tip: function (r) {
      if (r.ell_share == null) return { lines: [['English learners', 'not yet counted']], note: '' };
      return { lines: [['Oyster River', num(r.ell) + ' students'], ['New Hampshire', num(r.ell_nh) + ' students'], ['Share of ORCSD enrollment', p1(r.ell_share)]], note: 'Students eligible for English language assistance. Source: NH DOE, as printed in the ORCSD annual reports.' };
    }
  };
  ROWS.efa = {
    aria: 'Education Freedom Account students living in Durham, Lee and Madbury, by fiscal year',
    domain: [0, 120], ticks: [0, 25, 50, 75, 100], axis: false,
    tickFmt: function (v) { return String(v); },
    series: [{ id: 'efa', get: function (r) { return r.efa_tot; }, main: true }],
    label: function (r) {
      if (r.efa_tot == null) return nodata(r.fy < '2021-22' ? 'Program began in 2021-22' : 'Not yet reported', 'efa_tot', 'derived');
      return { big: num(r.efa_tot), sub: 'Residents using Education Freedom Accounts', delta: 'Durham ' + num(r.efa_dur) + ' · Lee ' + num(r.efa_lee) + ' · Madbury ' + num(r.efa_mad), tag: 'Actual', prov: false, src: 'derived', field: 'efa_tot' };
    },
    tip: function (r) {
      if (r.efa_tot == null) return { lines: [['Education Freedom Accounts', 'none before 2021-22']], note: '' };
      return { lines: [['Durham', r.efa_dur.toFixed(1)], ['Lee', r.efa_lee.toFixed(1)], ['Madbury', r.efa_mad.toFixed(1)], ['State cost of an adequate education for them', money(r.efa_aid)]], note: 'Residents of the three towns who hold an account, from the DOE’s by-municipality reports (dated June 2022 to October 2026). Early reports count part-year students in proportion, so years are not strictly comparable. Not every account holder left an Oyster River school.' };
    }
  };
  ROWS.drop = {
    aria: 'Oyster River students who dropped out, by fiscal year',
    domain: [0, 5], ticks: [0, 2, 4], axis: false,
    tickFmt: function (v) { return String(v); },
    series: [{ id: 'dr', get: function (r) { return r.drop; }, main: true }],
    label: function (r) {
      if (r.drop == null) return nodata('Not yet reported', 'drop');
      return { big: String(r.drop), sub: 'Students who dropped out', delta: 'NH ' + num(r.drop_nh) + ' statewide', tag: 'Actual', prov: false, src: 'years', field: 'drop' };
    },
    tip: function (r) {
      if (r.drop == null) return { lines: [['Dropouts', 'not yet reported']], note: '' };
      return { lines: [['Oyster River', String(r.drop)], ['New Hampshire (all districts)', num(r.drop_nh)]], note: 'Counts of students who left during the year or did not return by October 2. A count of one or two can change the line, so no trend should be read into it. Source: NH DOE, as printed in the ORCSD annual reports.' };
    }
  };
  ROWS.ctc = {
    aria: 'Oyster River High School students attending the Tri-City Career Technology Center, by fiscal year',
    domain: [0, 110], ticks: [0, 25, 50, 75, 100], axis: false,
    tickFmt: function (v) { return String(v); },
    series: [{ id: 'ctc', get: function (r) { return r.ctc; }, main: true }],
    label: function (r) {
      if (r.ctc == null) return nodata('Not yet reported', 'ctc');
      return { big: String(r.ctc), sub: 'High school students in career technology', delta: '', tag: 'Actual', prov: false, src: 'years', field: 'ctc' };
    },
    tip: function (r) {
      if (r.ctc == null) return { lines: [['Career technology', 'not yet reported']], note: '' };
      return { lines: [['Students at Tri-City', String(r.ctc)]], note: 'Students attending the Tri-City Career Technology Centers for hands-on technical programs. Tuition and transportation for these students are paid by the district. Source: ORHS guidance office, as printed in the ORCSD annual reports.' };
    }
  };
  ROWS.tdeg = {
    aria: 'Share of Oyster River professional staff with a master’s degree or higher, compared with New Hampshire, by fiscal year',
    domain: [55, 90], ticks: [60, 70, 80], axis: false,
    tickFmt: function (v) { return v + '%'; },
    series: [
      { id: 'nh', get: function (r) { return r.td_adv_nh; }, comp: true },
      { id: 'orc', get: function (r) { return r.td_adv; }, main: true }
    ],
    label: function (r) {
      if (r.td_adv == null) return nodata(r.fy === '2019-20' ? 'Not printed for 2019-20' : 'Not yet reported', 'td_adv', 'derived');
      return { big: p1(r.td_adv), sub: 'Teachers with a master’s degree or higher', delta: 'NH ' + p1(r.td_adv_nh), tag: 'Actual', prov: false, src: 'derived', field: 'td_adv' };
    },
    tip: function (r) {
      if (r.td_adv == null) return { lines: [['Teacher degrees', 'not available']], note: '' };
      return { lines: [['Bachelor’s only', r.td_b.toFixed(1) + '% (NH ' + r.td_b_nh.toFixed(1) + '%)'], ['Master’s', r.td_m.toFixed(1) + '% (NH ' + r.td_m_nh.toFixed(1) + '%)'], ['Beyond master’s', r.td_x.toFixed(1) + '% (NH ' + r.td_x_nh.toFixed(1) + '%)']], note: 'Share of full-time-equivalent professionals: teachers, guidance, special education, library and nursing staff. Source: NH DOE, as printed in the ORCSD annual reports.' };
    }
  };
  ROWS.texp = {
    aria: 'Oyster River staff with 14 or more years of experience, by fiscal year',
    domain: [100, 170], ticks: [110, 130, 150], axis: false,
    tickFmt: function (v) { return String(v); },
    series: [{ id: 'tx', get: function (r) { return r.tx_tot; }, main: true }],
    label: function (r) {
      if (r.tx_tot == null) return nodata('Not printed for this year', 'tx_tot', 'derived');
      return { big: String(r.tx_tot), sub: 'Staff with 14 or more years of experience', delta: 'Mast Way ' + r.tx_mw + ' · Moharimet ' + r.tx_mo + ' · Middle ' + r.tx_ms + ' · High ' + r.tx_hs, tag: 'Actual', prov: false, src: 'derived', field: 'tx_tot' };
    },
    tip: function (r) {
      if (r.tx_tot == null) return { lines: [['Experienced staff', 'not available']], note: '' };
      return { lines: [['Mast Way', String(r.tx_mw)], ['Moharimet', String(r.tx_mo)], ['Middle school', String(r.tx_ms)], ['High school', String(r.tx_hs)], ['Total', String(r.tx_tot)]], note: 'Counts of professional staff with 14 or more years of experience, by school. Source: school district office, as printed in the ORCSD annual reports.' };
    }
  };
  ROWS.attlvl = {
    aria: 'Attendance rate averaged across school levels, Oyster River and New Hampshire, by fiscal year',
    domain: [89, 99], ticks: [90, 93, 96, 99], axis: false,
    tickFmt: function (v) { return v + '%'; },
    series: [
      { id: 'nh', get: function (r) { return r.at_s; }, comp: true },
      { id: 'orc', get: function (r) { return r.at_d; }, main: true }
    ],
    label: function (r) {
      if (r.at_d == null) return nodata(r.atx_k != null ? 'Printed in the report but not plotted' : 'Not yet reported', 'at_d', 'derived');
      return { big: p1(r.at_d), sub: 'Attendance, average of four school levels', delta: 'NH ' + p1(r.at_s), tag: 'Actual', prov: false, src: 'derived', field: 'at_d' };
    },
    tip: function (r) {
      if (r.at_d == null) {
        if (r.atx_k == null) return { lines: [['Attendance by level', 'not yet reported']], note: '' };
        return { lines: [['Printed in the report', r.atx_k + '% K · ' + r.atx_e + '% elementary · ' + r.atx_m + '% middle · ' + r.atx_h + '% high']], note: r.fy === '2023-24' ? 'The district’s report prints exactly the same figures for 2022-23 and 2023-24, for the district and for the state, so this year looks like a repeat.' : 'These figures jump to about 98% for both the district and the state, which looks like a change in how the DOE measures attendance, so they are not compared with earlier years.' };
      }
      function ln(a, b) { return a.toFixed(1) + '% (NH ' + b.toFixed(1) + '%)'; }
      return { lines: [['Kindergarten', ln(r.at_k, r.at_k_nh)], ['Elementary', ln(r.at_e, r.at_e_nh)], ['Middle school', ln(r.at_m, r.at_m_nh)], ['High school', ln(r.at_h, r.at_h_nh)]], note: 'Actual attendance divided by membership, by level. The line is the simple average of the four levels. Source: NH DOE, as printed in the ORCSD annual reports.' };
    }
  };
  ROWS.proj = {
    aria: 'Actual October 1 enrollment compared with NESDEC and district planning committee projections, by fiscal year',
    domain: [1950, 2200], ticks: [2000, 2100, 2200], axis: false,
    tickFmt: function (v) { return num(v); },
    series: [
      { id: 'lrpc', get: function (r) { return r.pr_lrpc; }, comp: true },
      { id: 'nes', get: function (r) { return r.pr_nes; }, alt: 'square' },
      { id: 'act', get: function (r) { return r.enrollment; }, main: true }
    ],
    label: function (r) {
      if (r.pr_nes == null && r.pr_lrpc == null) return { big: r.enrollment != null ? num(r.enrollment) : '—', sub: 'Enrollment, no projection printed for this year', delta: '', tag: r.enrollment != null ? 'Actual' : 'No data', prov: r.enrollment == null, src: 'years', field: 'enrollment' };
      var act = function (p, who) { return r.enrollment != null ? 'Actual ' + num(r.enrollment) + ' (' + signPct((r.enrollment / p - 1) * 100) + ' vs ' + who + ')' : ''; };
      if (r.pr_nes == null) return { big: num(r.pr_lrpc), sub: 'District committee projected enrollment, K-12', delta: act(r.pr_lrpc, 'committee'), tag: 'Projection', prov: true, src: 'years', field: 'pr_lrpc' };
      var d = r.enrollment != null ? ' · ' + act(r.pr_nes, 'NESDEC') : '';
      return { big: num(r.pr_nes), sub: 'NESDEC projected enrollment, K-12', delta: 'District committee ' + num(r.pr_lrpc) + d, tag: 'Projection', prov: true, src: 'years', field: 'pr_nes' };
    },
    tip: function (r) {
      if (r.pr_nes == null && r.pr_lrpc == null) return { lines: [['Projections', 'none printed for this year']], note: 'The district’s annual reports print projections for 2018-19 to 2027-28.' };
      var L = [];
      if (r.pr_nes != null) L.push(['NESDEC projection', num(r.pr_nes)]);
      if (r.pr_lrpc != null) L.push(['District committee projection', num(r.pr_lrpc)]);
      if (r.enrollment != null) L.push(['Actual October 1', num(r.enrollment)]);
      return { lines: L, note: 'Each year shows the latest projection printed before that school year began, from the district’s 2018 to 2024 annual reports. NESDEC is the New England School Development Council, which the district uses for enrollment forecasts; its tables appear in the 2021 to 2024 reports only. The committee is the district’s Long Range Planning Committee. The 2024 report repeats the 2023 tables, and the 2025 and 2026 reports print none. For 2027-28 NESDEC projected 2,177 and the committee 1,981. The report prints the committee’s 2025-26 figure as 4,988, treated here as 1,988.' };
    }
  };
  ROWS.lvlenr.chg = { get: function (r) { return r.en_hs; }, kind: 'pct', note: 'high school' };
  ROWS.fb.chg = { get: function (r) { return r.fb_tot; }, kind: 'pct', note: 'total fund balance' };
  ROWS.cls.chg = { get: function (r) { return r.cs_d; }, kind: 'pct', note: 'average class size' };
  ROWS.sat.chg = { get: function (r) { return r.sat_tot; }, kind: 'pts', note: 'ORHS average' };
  ROWS.coll.chg = { get: function (r) { return r.col4; }, kind: 'pts', dec: true, note: 'four-year college' };
  ROWS.sped.chg = { get: function (r) { return r.sp_share; }, kind: 'pts', dec: true };
  ROWS.frl.chg = { get: function (r) { return r.frl_share; }, kind: 'pts', dec: true };
  ROWS.ell.chg = { get: function (r) { return r.ell_share; }, kind: 'pts', dec: true };
  ROWS.ctc.chg = { get: function (r) { return r.ctc; }, kind: 'pct', note: 'career technology students' };
  ROWS.tdeg.chg = { get: function (r) { return r.td_adv; }, kind: 'pts', dec: true, note: 'master’s or higher' };
  ROWS.texp.chg = { get: function (r) { return r.tx_tot; }, kind: 'pct', note: 'experienced staff' };
  ROWS.attlvl.chg = { get: function (r) { return r.at_d; }, kind: 'pts', dec: true };
  ROWS.proj.chg = { get: function (r) { return r.enrollment; }, kind: 'pct', note: 'actual enrollment' };

  function pend(field, src) { return { big: '—', sub: 'Not yet filed with the NH DOE', delta: '', tag: 'Pending', prov: true, src: src || 'derived', field: field }; }
  var DOEN = 'Source: DOE-25 District Profile (NH DOE), divided by October 1 enrollment.';
  ROWS.lvl = {
    money: true,
    aria: 'Actual cost per pupil by school level: elementary, middle and high school',
    domain: [16000, 26000], ticks: [16000, 20000, 24000], axis: false,
    tickFmt: function (v) { return '$' + v.toLocaleString('en-US'); },
    series: [
      { id: 'hs', get: function (r) { return r.cpp_hs; }, comp: true },
      { id: 'ms', get: function (r) { return r.cpp_ms; }, alt: 'square' },
      { id: 'el', get: function (r) { return r.cpp_el; }, main: true }
    ],
    label: function (r) {
      if (r.cpp_el == null) return pend('cpp_el', 'years');
      return { big: money(r.cpp_el), sub: 'Elementary schools, cost per pupil', delta: 'Middle ' + money(r.cpp_ms) + ' · High ' + money(r.cpp_hs), tag: 'Actual', prov: false, src: 'years', field: 'cpp_el' };
    },
    tip: function (r) {
      if (r.cpp_el == null) return { lines: [['Cost per pupil by level', 'not yet filed']], note: 'Appears after the district files its DOE-25.' };
      return { lines: [['Elementary', money(r.cpp_el)], ['Middle', money(r.cpp_ms)], ['High school', money(r.cpp_hs)], ['District total', money(r.nhed_cpp)]], note: 'Source: DOE-25 District Profile (NH DOE). Excludes construction and bond principal.' };
    }
  };
  ROWS.spec = {
    money: true,
    aria: 'Special education program spending per student by fiscal year',
    domain: [3000, 4000], ticks: [3000, 3500, 4000], axis: false,
    tickFmt: function (v) { return '$' + v.toLocaleString('en-US'); },
    series: [{ id: 'spec', get: function (r) { return r.spec_pps; }, main: true }],
    label: function (r) {
      if (r.spec_pps == null) return pend('spec_pps');
      return { big: money(r.spec_pps), sub: 'Special programs spending per student', delta: pct1(r.spec_share) + ' of operating spending', tag: 'Actual', prov: false, src: 'derived', field: 'spec_pps' };
    },
    tip: function (r) {
      if (r.spec_pps == null) return { lines: [['Special programs', 'not yet filed']], note: 'Appears after the district files its DOE-25.' };
      return { lines: [['Special programs spending', money(r.fn_spec)], ['Per October 1 student', money(r.spec_pps)], ['Share of operating spending', pct1(r.spec_share)]], note: 'Function 1200 (special programs), which includes special education and gifted programs. ' + DOEN };
    }
  };
  ROWS.adm = {
    aria: 'Administration and business services as a share of operating spending, by fiscal year',
    domain: [10, 15], ticks: [11, 12, 13, 14], axis: false,
    tickFmt: function (v) { return v + '%'; },
    series: [{ id: 'adm', get: function (r) { return r.adm_share; }, main: true }],
    label: function (r) {
      if (r.adm_share == null) return pend('adm_share');
      return { big: pct1(r.adm_share), sub: 'Administration and business ÷ operating spending', delta: moneyM(r.adm_amt, 1) + ' in total', tag: 'Actual', prov: false, src: 'derived', field: 'adm_share' };
    },
    tip: function (r) {
      if (r.adm_share == null) return { lines: [['Administration', 'not yet filed']], note: 'Appears after the district files its DOE-25.' };
      return { lines: [['General administration and business (2300, 2800)', moneyM(r.fn_gab, 2)], ['School administration (2400)', moneyM(r.fn_sadm, 2)], ['Business services (2500)', moneyM(r.fn_bus, 2)], ['Total', moneyM(r.adm_amt, 2) + ' · ' + pct1(r.adm_share)]], note: 'Share of total recurring expenditures. Source: DOE-25 District Profile.' };
    }
  };
  ROWS.bldg = {
    money: true,
    aria: 'Plant operations, transportation and bond interest per student by fiscal year',
    domain: [0, 2800], ticks: [0, 1000, 2000], axis: false,
    tickFmt: function (v) { return '$' + v.toLocaleString('en-US'); },
    series: [
      { id: 'debt', get: function (r) { return r.debt_pps; }, comp: true },
      { id: 'trans', get: function (r) { return r.trans_pps; }, alt: 'square' },
      { id: 'plant', get: function (r) { return r.plant_pps; }, main: true }
    ],
    label: function (r) {
      if (r.plant_pps == null) return pend('plant_pps');
      return { big: money(r.plant_pps), sub: 'Plant operations per student', delta: 'Buses ' + money(r.trans_pps) + ' · Bond interest ' + money(r.debt_pps), tag: 'Actual', prov: false, src: 'derived', field: 'plant_pps' };
    },
    tip: function (r) {
      if (r.plant_pps == null) return { lines: [['Buildings and buses', 'not yet filed']], note: 'Appears after the district files its DOE-25.' };
      return { lines: [['Plant operations', moneyM(r.fn_plant, 2) + ' · ' + money(r.plant_pps) + ' per student'], ['Transportation', moneyM(r.fn_trans, 2) + ' · ' + money(r.trans_pps) + ' per student'], ['Bond interest', moneyM(r.fn_bint, 2) + ' · ' + money(r.debt_pps) + ' per student']], note: 'Bond principal and construction are not included. ' + DOEN };
    }
  };
  ROWS.pay = {
    money: true,
    aria: 'Local property tax and state aid revenue per student by fiscal year',
    domain: [3000, 20000], ticks: [5000, 10000, 15000], axis: false,
    tickFmt: function (v) { return '$' + v.toLocaleString('en-US'); },
    series: [
      { id: 'state', get: function (r) { return r.state_pps; }, comp: true },
      { id: 'local', get: function (r) { return r.local_pps; }, main: true }
    ],
    label: function (r) {
      if (r.local_pps == null) return pend('local_pps');
      return { big: money(r.local_pps), sub: 'Local property tax revenue per student', delta: 'State aid ' + money(r.state_pps) + ' per student', tag: 'Actual', prov: false, src: 'derived', field: 'local_pps' };
    },
    tip: function (r) {
      if (r.local_pps == null) return { lines: [['Revenue per student', 'not yet filed']], note: 'Appears after the district files its DOE-25.' };
      return { lines: [['Local property tax', moneyM(r.rev_local, 1) + ' · ' + money(r.local_pps)], ['State aid (adequacy and other)', moneyM(r.state_aid_amt, 1) + ' · ' + money(r.state_pps)]], note: 'Per October 1 student. Source: DOE-25 District Profile revenue section.' };
    }
  };
  ROWS.aid = {
    money: true,
    aria: 'State adequacy aid: total state grant, the formula cost of an adequate education, and the school property tax the towns keep, by fiscal year',
    domain: [3e6, 10.8e6], ticks: [4e6, 6e6, 8e6, 10e6], axis: false,
    tickFmt: function (v) { return '$' + (v / 1e6) + 'M'; },
    series: [
      { id: 'cost', get: function (r) { return r.adq_cost; }, comp: true },
      { id: 'swept', get: function (r) { return r.adq_swept; }, alt: 'square' },
      { id: 'total', get: function (r) { return r.adq_total; }, main: true }
    ],
    label: function (r) {
      if (r.adq_total == null) return pend('adq_total');
      var est = r.adq_est;
      return { big: moneyM(r.adq_total, 2), sub: 'State adequacy grant, three towns' + (est ? ' (state estimate)' : ''), delta: r.adq_pct.toFixed(0) + '% of the ' + moneyM(r.adq_cost, 1) + ' formula cost', tag: est ? 'Estimate' : 'Actual', prov: est, src: 'years', field: 'adq_total' };
    },
    tip: function (r) {
      if (r.adq_total == null) return { lines: [['State adequacy aid', 'not available']], note: 'Appears when the state publishes it.' };
      var L = [];
      if (r.adq_base != null) {
        L.push(['Base adequacy (per pupil)', money(r.adq_base)]);
        L.push(['Free and reduced meal aid', money(r.adq_fr)]);
        L.push(['Special education aid', money(r.adq_sped)]);
        L.push(['English learner aid', money(r.adq_ell)]);
        if (r.adq_g3) L.push(['Grade 3 reading aid', money(r.adq_g3)]);
        if (r.adq_home) L.push(['Home education aid', money(r.adq_home)]);
      }
      L.push(['Formula cost of an adequate education', money(r.adq_cost)]);
      L.push(['School property tax the towns keep (SWEPT)', money(r.adq_swept) + ' · ' + r.adq_swept_pct.toFixed(0) + '% of grant']);
      L.push(['Grant paid on top of SWEPT', money(r.adq_total - r.adq_swept)]);
      L.push(['Total state grant', money(r.adq_total)]);
      if (r.adq_extra > 1) L.push(['Above formula cost (hold-harmless and targeted grants)', money(r.adq_extra)]);
      var n = r.adq_est ? 'State estimate: the district has not filed this year. ' : 'Matches the adequacy aid in the district DOE-25. ';
      return { lines: L, note: n + 'Sum of Durham, Lee and Madbury. Source: NH DOE Bureau of School Finance, adequate education aid files.' };
    }
  };
  ROWS.cmp = {
    money: true,
    aria: 'Oyster River cost per pupil compared with the New Hampshire average and the median K-12 district, by fiscal year',
    domain: [15000, 26000], ticks: [16000, 20000, 24000], axis: false,
    tickFmt: function (v) { return '$' + v.toLocaleString('en-US'); },
    series: [
      { id: 'avg', get: function (r) { return r.cpp_state_avg; }, comp: true },
      { id: 'med', get: function (r) { return r.cpp_k12_med; }, alt: 'square' },
      { id: 'orcsd', get: function (r) { return r.nhed_cpp; }, main: true }
    ],
    label: function (r) {
      if (r.cpp_state_avg == null) return pend('cpp_state_avg');
      return { big: (r.cpp_vs_avg >= 0 ? '+' : '−') + Math.abs(r.cpp_vs_avg).toFixed(1) + '%', sub: 'Cost per pupil vs. the NH average', delta: 'Rank ' + r.cpp_rank + ' of ' + r.cpp_rank_n + ' K-12 districts (1 = highest)', tag: 'Actual', prov: false, src: 'years', field: 'cpp_state_avg' };
    },
    tip: function (r) {
      if (r.cpp_state_avg == null) return { lines: [['Cost per pupil comparison', 'not yet published']], note: 'Appears after the DOE publishes cost per pupil.' };
      return { lines: [['Oyster River', money(r.nhed_cpp)], ['NH average', money(r.cpp_state_avg) + ' · ' + signPct(r.cpp_vs_avg)], ['Median K-12 district', money(r.cpp_k12_med) + ' · ' + signPct(r.cpp_vs_med)], ['Rank among K-12 districts', r.cpp_rank + ' of ' + r.cpp_rank_n]], note: 'Source: NH DOE Bureau of School Finance cost per pupil files. Median and rank are computed from the same file among districts that report elementary, middle and high school costs.' };
    }
  };
  ROWS.staff = {
    money: true,
    aria: 'Instruction staff salaries and benefits by fiscal year',
    domain: [6e6, 20e6], ticks: [8e6, 12e6, 16e6], axis: true,
    tickFmt: function (v) { return '$' + (v / 1e6) + 'M'; },
    series: [
      { id: 'ben', get: function (r) { return r.instr_ben; }, alt: 'square' },
      { id: 'sal', get: function (r) { return r.instr_sal; }, main: true }
    ],
    label: function (r) {
      if (r.instr_sal == null) return pend('instr_sal', 'years');
      return { big: moneyM(r.instr_sal, 1), sub: 'Instruction staff salaries', delta: 'Benefits ' + moneyM(r.instr_ben, 1), tag: 'Actual', prov: false, src: 'years', field: 'instr_sal' };
    },
    tip: function (r) {
      if (r.instr_sal == null) return { lines: [['Salaries and benefits', 'not yet filed']], note: 'Appears after the district files its DOE-25.' };
      return { lines: [['Salaries', money(r.instr_sal)], ['Benefits', money(r.instr_ben)], ['Total', money(r.instr_sal + r.instr_ben)]], note: 'Instruction accounts 1100 to 1400, general and special revenue funds. Source: DOE-25 Salaries-Benefits sheet.' };
    }
  };
  ROWS.sgp.chg = { get: function (r) { return r.sgp_rea; }, kind: 'pts', note: 'reading' };
  ROWS.grp.chg = { get: function (r) { return r.ela_iep; }, kind: 'pts', note: 'students with IEPs' };
  ROWS.att.chg = { get: function (r) { return r.att; }, kind: 'pts', dec: true };
  ROWS.rate.chg = { get: function (r) { return r.tax_dur; }, kind: 'pct', note: 'Durham' };
  ROWS.lvl.chg = { get: function (r) { return r.cpp_el; }, kind: 'pct', note: 'elementary' };
  ROWS.spec.chg = { get: function (r) { return r.spec_pps; }, kind: 'pct' };
  ROWS.adm.chg = { get: function (r) { return r.adm_share; }, kind: 'pts', dec: true };
  ROWS.bldg.chg = { get: function (r) { return r.plant_pps; }, kind: 'pct', note: 'plant operations' };
  ROWS.pay.chg = { get: function (r) { return r.local_pps; }, kind: 'pct', note: 'local property tax' };
  ROWS.aid.chg = { get: function (r) { return r.adq_total; }, kind: 'pct', note: 'total state grant' };
  ROWS.cmp.chg = { get: function (r) { return r.cpp_vs_avg; }, kind: 'pts', dec: true, note: 'gap vs. NH average' };
  ROWS.share.chg = { get: function (r) { return r.lsh_dur; }, kind: 'pts', note: 'Durham share' };
  ROWS.base.chg = { get: function (r) { return r.eq_pps; }, kind: 'pct', note: 'value per student' };
  ROWS.tstart.chg = { get: function (r) { return r.t_start; }, kind: 'pct', note: 'starting salary' };
  ROWS.tavg.chg = { get: function (r) { return r.t_avg; }, kind: 'pct', note: 'average salary' };
  ROWS.ratio.chg = { get: function (r) { return r.ratio; }, kind: 'pct', dec: true, note: 'students per teacher' };
  ROWS.staff.chg = { get: function (r) { return r.instr_sal; }, kind: 'pct', note: 'salaries' };
  var D0 = null;

  function setYearButtons() {
    document.querySelectorAll('.os-yr').forEach(function (b) {
      b.setAttribute('aria-pressed', String(+b.getAttribute('data-i') === sel));
    });
  }
  function redrawAll() {
    NAMES.forEach(function (k) { dash.draw('label-' + k); dash.draw('chart-' + k); dash.draw('src-' + k); });
  }
  function setSel(i) {
    sel = i;
    setYearButtons();

    redrawAll();
  }

  function autoDom(spec, D) {
    var vs = [];
    spec.series.forEach(function (s) { D.forEach(function (r) { var v = s.get(r); if (v != null) vs.push(v); }); });
    var lo = Math.min.apply(null, vs), hi = Math.max.apply(null, vs);
    var span = hi - lo, raw = span / 3;
    var p = Math.pow(10, Math.floor(Math.log10(raw)));
    var st = [1, 2, 2.5, 5, 10].map(function (m) { return m * p; }).filter(function (s) { return s >= raw; })[0];
    var d0 = Math.floor((lo - span * 0.08) / st) * st, d1 = Math.ceil((hi + span * 0.08) / st) * st;
    var ticks = [];
    for (var t = Math.ceil(d0 / st) * st; t < d1; t += st) ticks.push(t);
    return { domain: [d0, d1], ticks: ticks };
  }

  function renderChart(host, k, D) {
    var spec = ROWS[k];
    host.replaceChildren();
    host.style.position = 'relative';
    var W = Math.max(260, host.clientWidth || 560);
    var showX = true;
    var H = showX ? 150 : 128;
    var m = { l: k === 'budget' ? 58 : 50, r: 12, t: 10, b: showX ? 24 : 8 };
    var n = D.length;
    var pad = 16;
    var step = (W - m.l - m.r - pad * 2) / (n - 1);
    var x = function (i) { return m.l + pad + i * step; };
    var dm = (mode !== 'nom' && spec.money) ? autoDom(spec, D) : { domain: spec.domain, ticks: spec.ticks };
    var d0 = dm.domain[0], d1 = dm.domain[1];
    var y = function (v) { return m.t + (H - m.t - m.b) * (1 - (v - d0) / (d1 - d0)); };

    var svg = svgEl('svg', { viewBox: '0 0 ' + W + ' ' + H, width: '100%', height: H, role: 'img', 'aria-label': spec.aria });
    host.appendChild(svg);

    // selected band
    svgEl('rect', { x: x(sel) - step / 2, y: 0, width: step, height: H - m.b + 6, rx: 6, fill: 'var(--rc)', 'fill-opacity': 0.13 }, svg);
    // column guides
    D.forEach(function (r, i) { svgEl('line', { x1: x(i), x2: x(i), y1: m.t - 4, y2: H - m.b, class: 'gl' }, svg); });
    // y ticks
    dm.ticks.forEach(function (t, j) {
      var yy = y(t);
      svgEl('line', { x1: m.l, x2: W - m.r, y1: yy, y2: yy, class: j === 0 ? 'bl' : 'gl' }, svg);
      var tx = svgEl('text', { x: m.l - 8, y: yy + 4, 'text-anchor': 'end', class: 'ax' }, svg);
      tx.textContent = spec.tickFmt(t);
    });
    // x labels
    if (showX) {
      D.forEach(function (r, i) {
        var tx = svgEl('text', { x: x(i), y: H - 6, 'text-anchor': 'middle', class: 'ax' + (i === sel ? ' on' : '') }, svg);
        tx.textContent = (step >= 38 ? 'FY' : '\u2019') + r.short.slice(3);
      });
    }
    // no-test marks
    D.forEach(function (r, i) {
      if (r.no_test && spec.noTestMark) {
        var nt = svgEl('text', { x: x(i), y: (m.t + H - m.b) / 2 + 3, 'text-anchor': 'middle', class: 'nt' }, svg);
        nt.textContent = 'no test';
      }
    });
    // series
    spec.series.forEach(function (s) {
      var pts = [];
      D.forEach(function (r, i) {
        var v = s.get(r);
        if (v != null) pts.push({ i: i, v: v, r: r });
      });
      var color = s.comp ? 'var(--color-fg-muted)' : 'var(--rc)';
      var j;
      for (j = 1; j < pts.length; j++) {
        var a = pts[j - 1], b = pts[j];
        if (b.i - a.i > 1) continue;
        var dotted = s.main && s.prov && (s.prov(a.r) || s.prov(b.r));
        svgEl('line', {
          x1: x(a.i), y1: y(a.v), x2: x(b.i), y2: y(b.v),
          stroke: color, 'stroke-width': s.comp ? 1.5 : (s.alt ? 1.8 : 2.4), 'stroke-linecap': 'round',
          'stroke-dasharray': s.comp ? '5 4' : (s.alt ? '7 3 1 3' : (dotted ? '1.5 5' : 'none'))
        }, svg);
      }
      pts.forEach(function (p) {
        var on = p.i === sel;
        var hollow = s.comp || (s.prov && s.prov(p.r));
        var fill = hollow ? 'var(--color-panel)' : color;
        var cx = x(p.i), cy = y(p.v);
        if (s.comp) {
          var q = on ? 6 : 4.5;
          svgEl('polygon', { points: cx + ',' + (cy - q) + ' ' + (cx + q) + ',' + cy + ' ' + cx + ',' + (cy + q) + ' ' + (cx - q) + ',' + cy, fill: fill, stroke: color, 'stroke-width': 1.6 }, svg);
        } else if (s.alt) {
          var q2 = on ? 5.5 : 4;
          svgEl('rect', { x: cx - q2, y: cy - q2, width: q2 * 2, height: q2 * 2, rx: 1.5, fill: color, 'fill-opacity': 0.9, stroke: 'var(--color-panel)', 'stroke-width': 1.2 }, svg);
        } else {
          svgEl('circle', { cx: cx, cy: cy, r: on ? 6 : 3.6, fill: fill, stroke: on ? 'var(--color-panel)' : color, 'stroke-width': on ? 2 : 1.8 }, svg);
          if (on && hollow) svgEl('circle', { cx: cx, cy: cy, r: 6, fill: 'none', stroke: color, 'stroke-width': 2 }, svg);
        }
      });
    });

    // tooltip
    var tip = div('os-tip');
    tip.hidden = true;
    host.appendChild(tip);
    function showTip(i) {
      var r = D[i];
      var t = spec.tip(r);
      tip.replaceChildren();
      var h = document.createElement('h4');
      h.textContent = 'FY ' + r.fy;
      tip.appendChild(h);
      var st = document.createElement('span');
      st.className = 'st';
      st.textContent = stat(r);
      tip.appendChild(st);
      var dl = document.createElement('dl');
      t.lines.forEach(function (ln) {
        var dt = document.createElement('dt'); dt.textContent = ln[0];
        var dd = document.createElement('dd'); dd.textContent = ln[1];
        dl.appendChild(dt); dl.appendChild(dd);
      });
      tip.appendChild(dl);
      if (t.note) { var p = document.createElement('p'); p.textContent = t.note; tip.appendChild(p); }
      if (mode !== 'nom' && spec.money) {
        var M = MODES[mode];
        var u = mode === 'cpi' ? 'months' : 'quarters';
        var extra = '';
        if (r.partial) extra = (mode === 'cpi' && r.n_used === 11) ? ' The index averages 11 of 12 months because no October 2025 CPI was published.' : ' The index averages only the ' + r.n_used + ' of ' + M.nn + ' ' + u + ' published so far.';
        var p2 = document.createElement('p');
        p2.textContent = 'Shown in FY 2024-25 dollars, adjusted with ' + M.label + '.' + extra;
        tip.appendChild(p2);
      }
      tip.hidden = false;
      var tw = tip.offsetWidth, th = tip.offsetHeight;
      var left = x(i) + step / 2 + 6;
      if (left + tw > W) left = x(i) - step / 2 - 6 - tw;
      if (left < 0) left = Math.max(0, Math.min(W - tw, x(i) - tw / 2));
      tip.style.left = left + 'px';
      tip.style.top = Math.max(0, Math.min(H - th, 6)) + 'px';
    }
    D.forEach(function (r, i) {
      var hit = svgEl('rect', { x: x(i) - step / 2, y: 0, width: step, height: H, class: 'hit' }, svg);
      hit.addEventListener('pointerenter', function () { showTip(i); });
      hit.addEventListener('pointerleave', function (e) { if (e.pointerType === 'mouse') tip.hidden = true; });
      hit.addEventListener('click', function () { setSel(i); });
    });
    svg.addEventListener('pointerleave', function (e) { if (e.pointerType === 'mouse') tip.hidden = true; });
  }

  function renderLabel(host, k, D) {
    var r = D[sel];
    var L = ROWS[k].label(r);
    var real = mode !== 'nom' && ROWS[k].money;
    if (real) L.sub += ' · FY 2024-25 dollars';
    host.replaceChildren();
    var big = div('os-big', L.big);
    if (!real) {
      big.setAttribute('data-source', L.src);
      big.setAttribute('data-field', L.field);
      big.setAttribute('data-where', 'fy=' + r.fy);
    }
    host.appendChild(big);
    host.appendChild(div('os-sub', L.sub));
    var C = ROWS[k].chg;
    if (C && !(L.delta && /since/.test(L.delta))) {
      var cur = C.get(r), bi = -1, i;
      for (i = 0; i < D.length; i++) { if (C.get(D[i]) != null) { bi = i; break; } }
      if (cur != null && bi >= 0) {
        var txt;
        if (D[sel] === D[bi]) txt = 'Base year' + (bi > 0 ? ' (FY ' + D[bi].fy + ')' : '');
        else {
          var d = C.kind === 'pct' ? (cur / C.get(D[bi]) - 1) * 100 : cur - C.get(D[bi]);
          var mag = Math.abs(d);
          var u = C.kind === 'pct' ? '%' : (C.unit ? ' ' + C.unit : (Math.abs(mag - 1) < 0.05 ? ' point' : ' points'));
          var num1 = (C.kind === 'pct' || C.dec) ? mag.toFixed(1) : String(Math.round(mag));
          txt = (mag < 0.05 ? '▬ No change' : arrow(d) + ' ' + num1 + u) + ' since FY ' + D[bi].fy + (C.note ? ' (' + C.note + ')' : '');
        }
        host.appendChild(div('os-delta os-chg', txt));
      }
    }
    if (L.delta) host.appendChild(div('os-delta', L.delta));
    var tag = div('os-tag' + (L.prov ? ' is-prov' : ''), L.tag);
    host.appendChild(tag);
  }

  NAMES.forEach(function (k) {
    dash.draw('chart-' + k, function (el) {
      var D = getData();
      if (!D) { el.textContent = '—'; return; }
      renderChart(el, k, D);
    });
    dash.draw('label-' + k, function (el) {
      var D = getData();
      if (!D) { el.textContent = '—'; return; }
      renderLabel(el, k, D);
    });
  });


  // ---- Direct source links for the selected year ----
  var SRC = window.__SRC.SRC;
  var SRCMAP = window.__SRC.MAP;
  var BUDED = { 2018: '2018', 2019: '2019', 2020: '2020', 2021: '2020', 2022: '2021', 2023: '2022', 2024: '2023' };
  function srcKey(s, r) {
    var y = parseInt(r.fy, 10);
    if (s.k === 'fy') return r.fy;
    if (s.k === 'ty') return String(y);
    if (s.k === 'ef') return String(r.adm_file);
    if (s.k === 'endy') return String(y + 1);
    if (s.k === 'ar') return String(Math.min(2026, y + 2));
    if (s.k === 'bud') return BUDED[y + 1] || null;
    if (s.k === 'arap') return y + 1 <= 2024 ? String(y + 1) : null;
    if (s.k === 'arv') return y + 1 >= 2018 && y + 1 <= 2027 ? String(y + 1) : null;
    if (s.k === 'arp') return y >= 2018 && y <= 2024 ? String(y) : null;
    return null;
  }
  function fileExt(u) { var m = /\.(csv|pdf|xlsx|xls)(?:$|\?)/i.exec(u); return m ? m[1].toUpperCase() : (/DownloadRecords/.test(u) ? 'XLSX' : ''); }
  function aLink(href, text) {
    var a = document.createElement('a');
    a.href = href; a.target = '_blank'; a.rel = 'noopener'; a.textContent = text;
    return a;
  }
  function renderSrc(host, k, D) {
    var r = D[sel];
    var has = ROWS[k].label(r).big !== '\u2014';
    host.replaceChildren();
    host.appendChild(document.createTextNode('Data: '));
    var first = true, shown = {};
    function sep() { if (!first) host.appendChild(document.createTextNode(' \u00b7 ')); first = false; }
    (SRCMAP[k] || []).forEach(function (id) {
      var s = SRC[id], url = null, text = null, kk;
      if (s.k === 'one') { url = s.u; text = s.n; }
      else if (s.k === 'page') { url = s.page; text = s.pn; }
      else if (has && (kk = srcKey(s, r)) && s.m[kk]) {
        url = s.m[kk];
        text = s.k === 'arv' && kk === '2027' ? 'ORCSD official results, March 10, 2026' : s.n + ', ' + (/^ar/.test(s.k) || s.k === 'bud' ? kk + ' edition' : (s.lab || 'FY ') + (s.k === 'fy' ? r.fy : (s.lb ? s.lb[kk] : kk)));
        var x = fileExt(url); if (x) text += ' (' + x + ')';
      }
      if (!url) { if (shown[s.page]) return; shown[s.page] = 1; }
      sep();
      if (url) host.appendChild(aLink(url, text));
      else { host.appendChild(aLink(s.page, s.pn)); host.appendChild(document.createTextNode(' (no file for this year)')); }
    });
    sep();
    var all = aLink('#os-sources', 'all files by year');
    all.addEventListener('click', function () { var d = document.getElementById('os-sources'); if (d && d.tagName === 'DETAILS') d.open = true; else { var p = d && d.closest('details'); if (p) p.open = true; } });
    host.appendChild(all);
  }
  NAMES.forEach(function (k) {
    dash.draw('src-' + k, function (el) {
      var D = getData();
      if (!D) return;
      renderSrc(el, k, D);
    });
  });

  function headlineDraw(name, field, fmt) {
    dash.draw(name, function (el) {
      var h = dash.data('headline');
      if (h.status !== 'ok' || !h.data.length) { el.textContent = '—'; return; }
      el.setAttribute('data-source', 'headline');
      el.setAttribute('data-field', field);
      el.setAttribute('data-row', '0');
      el.textContent = fmt(h.data[0][field]);
    });
  }
  headlineDraw('t-spend', 'spend_pct', signPct);
  headlineDraw('t-spend-cpi', 'spend_cpi_pct', signPct);
  headlineDraw('t-spend-eci', 'spend_eci_pct', signPct);
  headlineDraw('t-cpp', 'cpp_pct', signPct);
  headlineDraw('t-cpp-cpi', 'cpp_cpi_pct', signPct);
  headlineDraw('t-cpp-eci', 'cpp_eci_pct', signPct);
  headlineDraw('t-enr', 'enrollment_pct', signPct);
  headlineDraw('t-elamin', 'ela_min', function (v) { return v + '%'; });
  headlineDraw('t-elamax', 'ela_max', function (v) { return v + '%'; });
  headlineDraw('t-stmin', 'state_min', function (v) { return v + '%'; });
  headlineDraw('t-stmax', 'state_max', function (v) { return v + '%'; });

  document.querySelectorAll('.os-yr').forEach(function (b) {
    b.addEventListener('click', function () { setSel(+b.getAttribute('data-i')); });
  });
  setYearButtons();

  var MODE_NOTE = {
    nom: 'Dollars as reported in each year, with no adjustment for inflation.',
    cpi: 'All dollar figures restated in FY 2024-25 dollars using the Northeast urban CPI-U (BLS), averaged July to June.',
    eci: 'All dollar figures restated in FY 2024-25 dollars using the BLS Employment Cost Index for state and local government education workers, a measure of what school labor costs, averaged July to June.'
  };
  dash.draw('modenote', function (el) { el.textContent = MODE_NOTE[mode]; });
  function setModeButtons() {
    document.querySelectorAll('.os-md').forEach(function (b) {
      b.setAttribute('aria-pressed', String(b.getAttribute('data-m') === mode));
    });
    dash.draw('modenote');
  }
  document.querySelectorAll('.os-md').forEach(function (b) {
    b.addEventListener('click', function () { mode = b.getAttribute('data-m'); setModeButtons(); redrawAll(); });
  });
  setModeButtons();

  // ---- Deep links: every section, row and note heading has an address (#ela, #who-pays, #notes-attendance)
  (function () {
    var root = document.querySelector('.os');
    if (!root) return;
    var SEC = {
      'Spending, enrollment and budget': 'spending',
      'Cost per student, and how it compares': 'cost-per-student',
      'Where the money goes': 'where-the-money-goes',
      'Who pays: local taxes, state aid and federal aid': 'who-pays',
      'How Durham, Lee and Madbury share the school bill': 'town-shares',
      'Who our students are': 'students',
      'How students are doing': 'results',
      'School climate and safety': 'climate-and-safety',
      'More detail': 'more-detail'
    };
    var ALIAS = { sources: 'os-sources', notes: 'os-notes' };
    var used = {};
    function slug(t) { return t.toLowerCase().replace(/[’']/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 56); }
    function claim(id) { var base = id, n = 2; while (used[id] || (document.getElementById(id) && !used[id] && document.getElementById(id).getAttribute('data-anchor') == null)) { id = base + '-' + n++; } used[id] = 1; return id; }
    var live = document.createElement('div');
    live.className = 'os-copied'; live.setAttribute('role', 'status'); live.setAttribute('aria-live', 'polite');
    root.appendChild(live);
    var liveT = 0;
    function say(msg) { live.textContent = msg; live.classList.add('on'); clearTimeout(liveT); liveT = setTimeout(function () { live.classList.remove('on'); live.textContent = ''; }, 2200); }
    function mk(id, label) {
      var a = document.createElement('a');
      a.className = 'os-anchor'; a.href = '#' + id; a.setAttribute('aria-label', 'Link to ' + label);
      a.title = 'Link to this ' + (label.length > 60 ? 'item' : 'item');
      a.innerHTML = '<svg width="14" height="14" viewBox="0 0 16 16" aria-hidden="true" focusable="false"><path d="M6.5 9.5l3-3M7 4.5l1-1a2.8 2.8 0 014 4l-1 1M9 11.5l-1 1a2.8 2.8 0 01-4-4l1-1" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>';
      a.addEventListener('click', function () {
        setTimeout(function () {
          try { if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(location.href).then(function () { say('Link copied'); }, function () {}); } catch (e) {}
        }, 0);
      });
      return a;
    }
    var toc = [];
    root.querySelectorAll('h2.os-h2').forEach(function (h) {
      var t = h.textContent.trim(), id = claim(SEC[t] || slug(t));
      h.id = id; h.setAttribute('data-anchor', '1'); h.classList.add('os-anch'); h.appendChild(mk(id, t));
      toc.push([id, t]);
    });
    root.querySelectorAll('section.os-row[data-k]').forEach(function (r) {
      var id = claim(r.getAttribute('data-k')), nm = r.querySelector('.os-name');
      r.id = id; r.setAttribute('data-anchor', '1');
      if (nm) {
        var lab = nm.textContent.trim(), sp = document.createElement('span');
        while (nm.lastChild && !(nm.lastChild.nodeType === 1 && nm.lastChild.classList.contains('os-dot'))) sp.insertBefore(nm.lastChild, sp.firstChild);
        sp.id = (nm.id || 'os-n-' + id) + '-t'; nm.appendChild(sp); r.setAttribute('aria-labelledby', sp.id);
        nm.classList.add('os-anch'); nm.appendChild(mk(id, lab));
      }
    });
    var notes = root.querySelector('details.os-notes');
    if (notes) {
      notes.id = 'os-notes'; notes.setAttribute('data-anchor', '1'); used['os-notes'] = 1;
      notes.querySelectorAll('h3').forEach(function (h) {
        var id = h.id || claim('notes-' + slug(h.textContent)); h.id = id; h.setAttribute('data-anchor', '1'); used[id] = 1;
        h.classList.add('os-anch'); h.appendChild(mk(id, h.textContent.trim()));
      });
    }
    var take = root.querySelector('.os-take');
    if (take && toc.length) {
      var nav = document.createElement('nav');
      nav.className = 'os-toc'; nav.setAttribute('aria-label', 'Jump to a section');
      nav.innerHTML = '<span class="os-toc-l">Jump to</span>' + toc.map(function (s) { return '<a href="#' + s[0] + '">' + s[1].replace(/&/g, '&amp;') + '</a>'; }).join('');
      take.parentNode.insertBefore(nav, take.nextSibling);
    }
    var hl = 0;
    function go(first) {
      var h = location.hash.replace(/^#/, '');
      if (!h) return;
      try { h = decodeURIComponent(h); } catch (e) {}
      var el = document.getElementById(ALIAS[h] || h);
      if (!el || !root.contains(el)) return;
      for (var d = el.closest('details'); d; d = d.parentElement && d.parentElement.closest('details')) d.open = true;
      el.scrollIntoView({ block: 'start', behavior: first ? 'auto' : 'smooth' });
      document.querySelectorAll('.is-target').forEach(function (x) { x.classList.remove('is-target'); });
      el.classList.add('is-target'); clearTimeout(hl); hl = setTimeout(function () { el.classList.remove('is-target'); }, 2600);
      if (!el.hasAttribute('tabindex')) el.setAttribute('tabindex', '-1');
      try { el.focus({ preventScroll: true }); } catch (e) {}
    }
    window.addEventListener('hashchange', function () { go(false); });
    go(true);
    window.addEventListener('load', function () { if (location.hash) go(true); });
  })();

  document.addEventListener('pointerdown', function (e) {
    if (e.pointerType !== 'mouse' && !(e.target.closest && e.target.closest('.os-chart'))) {
      document.querySelectorAll('.os-tip').forEach(function (t) { t.hidden = true; });
    }
  });
})();
