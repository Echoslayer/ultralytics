const cc = `https://app.codecov.io/gh/ultralytics/ultralytics/tree/${testAtlas.coverageCommit}/`;
const coverage = [['cfg',421,308],['data',3876,2575],['engine',3035,2136],['models',7533,3066],['nn',4557,3491],['optim',87,11],['solutions',1278,1027],['trackers',1711,1474],['utils',8219,5319]];
const needs = [
  ['predict','使用能力','讓圖片／影片產生可用結果','engine','engine/model.py','Model.predict → BasePredictor → 任務後處理','engine/predictor.py','test_python.py','比較來源類型、批次與 Results；繪圖與存檔分開檢查。'],
  ['data','使用能力','把自己的標註資料接進訓練','data','data/dataset.py','YOLODataset；先查格式與快取，再追增強','data/utils.py','test_python.py','公開小型資料：核對類別、空標註與轉換結果。'],
  ['train','使用能力','訓練、續訓與驗證模型','engine','engine/trainer.py','BaseTrainer 與任務 Trainer','engine/validator.py','test_engine.py','比較權重恢復、指標與設定；DDP／CUDA 需要真實設備。'],
  ['export','使用能力','部署到另一種執行環境','nn','engine/exporter.py','Exporter 與 EXPORT_ENVS → 匯出檔 → AutoBackend','nn/autobackend.py','test_exports.py','對應隔離環境比較輸出品質與速度；--export-env 只篩選、不安裝。'],
  ['track','使用能力','追蹤物件並做場景應用','trackers','trackers/track.py','追蹤 callback；區分偵測錯誤與 ID 切換','trackers/byte_tracker.py','test_solutions.py','固定短片：檢查遮擋、重新出現與跨串流狀態；計數另看 solutions。'],
  ['cfg','維護入口','調整 CLI 參數與使用說明','cfg','cfg/__init__.py','參數解析、型別集合與 _handle_deprecation','cfg/default.yaml','test_cli.py','核對 CLI／Python 一致性；參數修改同步 usage/cfg 與 macros。'],
  ['classify','貢獻調查','檢查分類圖片是否意外裁切','models','data/augment.py','classify_transforms / classify_augmentations','models/yolo/classify/predict.py','test_python.py','寬圖、長圖、方圖四角標記；比較 train／val／predict 真正輸入。既有研究候選，未證實為 bug。'],
  ['metrics','貢獻調查','定位 mAP 與結果品質差異','utils','utils/metrics.py','固定資料、任務與閾值，再追指標定義','engine/validator.py','test_python.py','保存預期與實際結果，先排除資料集、補邊與參數差異。']
];
const esc = s => String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const pct = r => (100*r[2]/r[1]).toFixed(2);
const source = p => `https://github.com/ultralytics/ultralytics/blob/${testAtlas.coverageCommit}/${p}`;
const link = p => `<a href="${source(p)}" target="_blank" rel="noopener">${esc(p)}</a>`;
const preview = deck.cards('map-preview',[{title:'先說需求',text:'使用能力、維護入口、貢獻調查分開看。'},{title:'找到負責模組',text:'入口 → 實作 → 既有測試。'},{title:'補足證據',text:'參考 Codecov，核對版本，再做真實驗證。'}]);
const reviewedFiles = testAtlas.files.filter(f=>f.review);
const fileIndex = new Map(testAtlas.files.map(f=>[f.path,f]));
const difficulty = ['容易','中等','困難'];
let requestedFile = null;
const covURL = f => `https://app.codecov.io/gh/ultralytics/ultralytics/blob/${testAtlas.coverageCommit}/${f.path}`;
const listHTML = items => `<ul>${items.map(x=>`<li>${esc(x)}</li>`).join('')}</ul>`;
const badge = (label,value) => `<span class="um-badge um-d${difficulty.indexOf(value)}">${label} ${esc(value||'未評估')}</span>`;
function fileDetail(f) {
  const r=f.review,c=f.coverage;
  const cov=c?`${c.percent.toFixed(2)}% · ${c.hits} / ${c.lines} 行 · ${c.misses} 行未覆蓋`:'未收錄於報告（不是 0%）';
  return `<div class="um-file-head"><small>${r?'已逐檔讀碼與查測試':'僅自動索引；尚未逐檔評估難度'}</small><h3>${esc(f.path)}</h3>${badge('修改',r?.changeDifficulty)} ${badge('補測試',r?.testDifficulty)}</div>
    <p class="um-cov"><strong>${cov}</strong><br><small>${f.sameSource?'工作檔與報告 commit 內容一致（含換行正規化比對）':c?'原碼不同：不映射函式漏行':f.path.startsWith('ultralytics/utils/callbacks/')?'pyproject.toml 明確排除 callbacks 的覆蓋收集':'此檔未出現在報告；可能無可執行行，不能當成 0%' }</small><br><a href="${c?covURL(f):cc+"ultralytics"}" target="_blank" rel="noopener">${c?"固定版本 Codecov":"報告總覽（未收錄此檔）"} ↗</a> · ${link(f.path)}</p>
    ${r?`<h4>為什麼這樣評估</h4><p>${esc(r.rationale)}</p><h4>修改會影響誰</h4><p>${esc(r.impact)}</p>
    <h4>從哪裡讀</h4><div class="um-symbols">${r.starts.map(s=>`<a href="${source(f.path)}#L${s.line}" target="_blank" rel="noopener"><code>${esc(s.name)}</code> L${s.line}</a>`).join('')}</div>
    <h4>依賴與執行門檻</h4>${listHTML(r.dependencies)}${r.blockers.length?listHTML(r.blockers):'<p>未識別額外硬體阻礙；仍需 repo 的基本依賴。</p>'}
    <h4>現有測試／下一站</h4>${r.existingTests.length?`<ul>${r.existingTests.map(t=>`<li><a href="${source(t.split('::')[0])}" target="_blank" rel="noopener"><code>${esc(t)}</code></a></li>`).join('')}</ul>`:'<p>本輪未找到可直接引用的測試；不等於完全沒有間接執行。</p>'}
    <h4>測試方案與既有回歸基線（本輪未執行）</h4>${listHTML(r.testIdeas)}${r.testEvidenceNote?`<p class="um-crosscheck">${esc(r.testEvidenceNote)}</p>`:""}<p class="um-muted">既有測試引用代表相關入口；不保證斷言覆蓋這裡每個分支。提案需與下方未覆蓋行對照。</p>`:'<p>此檔仍可查實際覆蓋率、符號與漏行。未實讀前不套用所在模組的難度結論。</p>'}
    ${f.crosscheck?.length?`<h4>二次查核：直接對上漏行的候選</h4>${f.crosscheck.map(x=>`<div class="um-crosscheck"><b>${esc(x.symbol)} · L${x.missingLines.join(', ')}</b><p>${esc(x.proposal)}</p><p>斷言：${esc(x.assertion)}</p><small>${esc(x.caution)}</small></div>`).join('')}`:''}
    <h4>Codecov 未覆蓋的函式／類別區段</h4><p class="um-muted">按漏行數排列；AST 只負責定位最內層符號。這是行覆蓋率，不是分支覆蓋率或 bug 清單。</p>
    ${f.gaps.length?f.gaps.map(g=>`<details class="um-gap"><summary><code>${esc(g.name)}</code><span>${g.lines.length} 行</span></summary><p>漏行：${g.lines.map(l=>`<a href="${source(f.path)}#L${l}" target="_blank" rel="noopener">${l}</a>`).join(' · ')}</p><pre>${g.examples.map(x=>`${x.line}  ${esc(x.code)}`).join('\n')}</pre></details>`).join(''):`<p>${c&&c.misses===0?'報告中所有可執行行都被執行過，仍可能缺少結果斷言。':'沒有可對應的逐行資料。'}</p>`}`;
}
function mountTests(root,state) {
  const el=root.querySelector('.um-tests'), list=el.querySelector('.um-list'), detail=el.querySelector('.um-detail');
  const defaults={query:'',module:'',change:'',test:'',cov:'',review:'reviewed',sort:'feasible',path:''};
  for(const [k,v] of Object.entries(defaults))state[k]??=v;
  if(requestedFile){state.path=requestedFile;state.query=requestedFile;state.review='';state.module='';state.change='';state.test='';state.cov='';requestedFile=null;}
  const controls=[...el.querySelectorAll('[data-filter]')];
  const sync=()=>controls.forEach(c=>c.value=state[c.dataset.filter]);
  function draw(){
    let rows=testAtlas.files.filter(f=>(!state.review||!!f.review)&&(!state.module||f.module===state.module)&&(!state.change||f.review?.changeDifficulty===state.change)&&(!state.test||f.review?.testDifficulty===state.test)&&(!state.cov||(state.cov==='missing'?f.coverage?.misses>0:state.cov==='low'?f.coverage&&f.coverage.percent<50:!f.coverage))&&[f.path,...f.symbolsIndex.map(s=>s.name),f.review?.rationale||''].join(' ').toLowerCase().includes(state.query.trim().toLowerCase()));
    rows.sort((a,b)=>state.sort==='coverage'?(a.coverage?.percent??101)-(b.coverage?.percent??101):state.sort==='misses'?(b.coverage?.misses??-1)-(a.coverage?.misses??-1):state.sort==='path'?a.path.localeCompare(b.path):(difficulty.indexOf(a.review?.testDifficulty??'')+4)%4-(difficulty.indexOf(b.review?.testDifficulty??'')+4)%4||(b.coverage?.misses??-1)-(a.coverage?.misses??-1));
    const f=rows.find(f=>f.path===state.path)||rows[0];if(f)state.path=f.path;
    el.querySelector('.um-count').textContent=`${rows.length} 個符合 · ${reviewedFiles.length} 檔深讀 / ${testAtlas.files.length} 檔索引 · ${testAtlas.totals.files} 檔有報告`;
    list.innerHTML=rows.map(f=>`<button data-file="${esc(f.path)}" aria-pressed="${f.path===state.path}"><b>${esc(f.path.replace('ultralytics/',''))}</b><span>${badge('改',f.review?.changeDifficulty)} ${badge('測',f.review?.testDifficulty)}</span><span>${f.coverage?`${f.coverage.percent.toFixed(2)}% · 缺 ${f.coverage.misses} 行`:'未收錄'}</span></button>`).join('');
    detail.innerHTML=f?fileDetail(f):'<h3>沒有符合的檔案</h3><p>清除條件，或切換「全部檔案」搜尋尚未深讀的區域。</p>';
  }
  const input=e=>{if(!e.target.dataset.filter)return;state[e.target.dataset.filter]=e.target.value;draw();};
  const click=e=>{const b=e.target.closest('button');if(!b)return;const file=b.dataset.file;if(b.hasAttribute('data-clear')){Object.assign(state,defaults);sync();}else if(file)state.path=file;else return;draw();detail.scrollTop=0;if(file)[...list.querySelectorAll('button')].find(b=>b.dataset.file===file)?.focus({preventScroll:true});};
  sync();draw();el.addEventListener('input',input);el.addEventListener('change',input);el.addEventListener('click',click);
  return()=>{el.removeEventListener('input',input);el.removeEventListener('change',input);el.removeEventListener('click',click);};
}
function mountNeeds(root,state) {
  const el=root.querySelector('.um-needs'), list=el.querySelector('.um-list'), detail=el.querySelector('.um-detail');
  const search=el.querySelector('input'), filter=el.querySelector('select');
  state.query ??= ''; state.kind ??= ''; state.id ??= 'predict'; search.value=state.query;filter.value=state.kind;
  function draw(){
    const rows=needs.filter(n=>(!state.kind||n[1]===state.kind)&&n.join(' ').toLowerCase().includes(state.query.toLowerCase()));
    list.innerHTML=`<p role="status">${rows.length} / ${needs.length} 個需求</p>`+rows.map(n=>`<button data-id="${n[0]}" aria-pressed="${state.id===n[0]}"><small>${n[1]}</small><b>${n[2]}</b><span>${n[3]} →</span></button>`).join('');
    if(!rows.length){detail.innerHTML='<h3>沒有符合的需求</h3><p>試試「推論」、「engine」或清除條件。</p>';return;}
    const n=rows.find(n=>n[0]===state.id)||rows[0];state.id=n[0];
    const cov=coverage.find(r=>r[0]===n[3]);
    detail.innerHTML=`<small>${n[1]} · 閱讀路線，非完整呼叫圖</small><h3>${n[2]}</h3><p class="um-route">需求 → ${n[3]} → 驗證</p><details open><summary>01 · 入口與閱讀重點</summary><p>${link('ultralytics/'+n[4])}</p><p>${n[5]}</p><p>下一站：${link('ultralytics/'+n[6])}</p></details><details open><summary>02 · 驗證與既有測試入口</summary><p>${n[8]}</p><p>${link('tests/'+n[7])}（相關測試檔，不表示已覆蓋此情境）</p></details><p class="um-cov"><a href="${cc+encodeURIComponent('ultralytics/'+n[3])}" target="_blank" rel="noopener">${n[3]} 覆蓋率 ${pct(cov)}% ↗</a> · 未覆蓋 ${cov[1]-cov[2]} 行<br><small>模組彙總，不能推論這條需求的覆蓋率。報告 bb3e155；查核 2026-10-28。</small></p>`;
    list.querySelectorAll('[data-id]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.id===state.id));
  }
  const input=()=>{state.query=search.value;state.kind=filter.value;draw();};
  const click=e=>{const b=e.target.closest('button');if(!b)return;if(b.hasAttribute('data-clear')){state.query='';state.kind='';search.value='';filter.value='';}else if(b.dataset.id)state.id=b.dataset.id;draw();};
  el.addEventListener('input',input);el.addEventListener('change',input);el.addEventListener('click',click);draw();
  return ()=>{el.removeEventListener('input',input);el.removeEventListener('change',input);el.removeEventListener('click',click);};
}
function mountTree(root,state){
  const el=root.querySelector('.um-tree');state.path ??= '';state.query ??= '';state.level ??= '';state.fileOpen ??= {};
  const search=el.querySelector('input'),filter=el.querySelector('select');search.value=state.query;filter.value=state.level;
  function draw(){
    const current=atlas.nodes.find(n=>n.path===state.path),parts=state.path.split('/').filter(Boolean);
    el.querySelector('.um-crumbs').innerHTML=`<button data-path="">repo</button>`+parts.map((p,i)=>` / <button data-path="${parts.slice(0,i+1).join('/')}">${esc(p)}</button>`).join('');
    const rows=atlas.nodes.filter(n=>n.path&&(state.query?(n.path+' '+n.role).toLowerCase().includes(state.query.toLowerCase()):n.parent===state.path)&&(!state.level||n.level===state.level));
    el.querySelector('.um-list').innerHTML=`<p role="status">${rows.length} 個目錄 · ${state.query?'全圖搜尋':'本層'}</p>`+rows.map(n=>`<button data-path="${n.path}"><small>${n.level}</small><b>${esc(n.path)}</b><span>${n.role}</span></button>`).join('')+(!rows.length?'<p>沒有符合的目錄；可清除條件或返回上層。</p>':'');
    const childDirs=atlas.nodes.some(n=>n.parent===state.path&&n.path);
    const extra=reviewedFiles.filter(f=>f.path.split('/').slice(0,-1).join('/')===state.path||(!childDirs&&state.path&&f.path.startsWith(state.path+'/'))).map(f=>f.path);
    const entries=[...new Set([...extra,...current.files])];
    el.querySelector('.um-detail').innerHTML=`<small>${current.level}${current.inherited?' · 目錄閱讀級別沿用上層；檔案難度另評':''}</small><h3>${esc(current.path||'Ultralytics')}</h3><p>${current.role}</p><p>閱讀級別不是修改難度。展開檔案查看實讀結果，或前往測試地圖比較。</p><h4>重要檔案與閱讀入口</h4>${entries.map(p=>{const f=fileIndex.get(p);return `<details data-file-card="${esc(p)}"${state.fileOpen[p]?' open':''}><summary>${esc(p.replace(state.path+'/',''))}${f?.review?` ${badge('修改',f.review.changeDifficulty)} ${badge('測試',f.review.testDifficulty)}`:''}</summary>${f?fileDetail(f):`<p>${link(p)}</p><p>設定／文件入口；不屬於 Python 行覆蓋率報告。</p>`}${f?`<button class="um-next-file" data-open-test="${esc(p)}">下一站：在測試地圖比較這個檔案 →</button>`:''}</details>`;}).join('')||'<p>選擇子目錄以尋找具體檔案。</p>'}<p class="um-muted">${current.deeper?'更深路徑的已審查檔案會列在終端目錄卡片；測試地圖可搜尋所有 Python 檔。':'沒有更深的已追蹤目錄。'}</p>`;
  }
  const input=()=>{state.query=search.value;state.level=filter.value;draw();};
  const click=e=>{const b=e.target.closest('button');if(!b)return;if(b.dataset.openTest){requestedFile=b.dataset.openTest;location.hash='test-map';return;}if(b.hasAttribute('data-path')){state.path=b.dataset.path;state.query='';search.value='';}else if(b.hasAttribute('data-up')){state.path=state.path.split('/').slice(0,-1).join('/');}else if(b.hasAttribute('data-clear')){state.query='';state.level='';search.value='';filter.value='';}draw();};
  const toggle=e=>{if(e.target.dataset.fileCard)state.fileOpen[e.target.dataset.fileCard]=e.target.open;};
  el.addEventListener('input',input);el.addEventListener('change',input);el.addEventListener('click',click);el.addEventListener('toggle',toggle,true);draw();return()=>{el.removeEventListener('input',input);el.removeEventListener('change',input);el.removeEventListener('click',click);el.removeEventListener('toggle',toggle,true);};
}
const testsPreview = `<div class="um-test-preview" data-key="test-map-preview"><h3>逐檔決定：改得動，也驗得了</h3><p>${reviewedFiles.length} 檔實讀評估 · ${testAtlas.files.length} 檔 Python 索引 · ${testAtlas.totals.files} 檔 Codecov</p><div class="um-preview-grid">${reviewedFiles.filter(f=>['ultralytics/nn/modules/activation.py','ultralytics/engine/trainer.py','ultralytics/utils/files.py','ultralytics/optim/muon.py'].includes(f.path)).map(f=>`<article><b>${esc(f.path.replace('ultralytics/',''))}</b><p>${badge('修改',f.review.changeDifficulty)} ${badge('測試',f.review.testDifficulty)}</p><strong>${f.coverage?.percent.toFixed(2)??'—'}%</strong><p>${esc(f.review.rationale)}</p></article>`).join('')}</div><p>HTML 可篩選、排序、看函式漏行與具體測例；靜態匯出保留此代表狀態。</p></div>`;
const story={title:'Ultralytics · Repo 與測試需求地圖',label:'ULTRALYTICS / CONTRIBUTOR ATLAS',pages:[
  deck.cover({title:'Ultralytics<br>找出改得動、驗得了的檔案',meta:`Repo 介紹 × 逐檔測試需求 × Codecov<br>${reviewedFiles.length} 檔實讀 · ${testAtlas.totals.files} 檔覆蓋率 · 2026-10-28`,instruction:'先理解 repo，再用修改難度、補測試成本和實際漏行選切入點。'}),
  {id:'intro',section:'01 / REPO 介紹',title:'把視覺模型從資料帶到應用',lead:'Python 套件與 yolo CLI，共用模型生命週期。',art:deck.cards('intro',[{title:'要回答什麼',text:'detect 偵測 · segment 實例分割 · semantic 語意分割 · depth 深度 · classify 分類 · pose 姿態 · obb 旋轉框。'},{title:'怎麼操作',text:'train → val → predict → export → track → benchmark<br>訓練、驗證、推論、匯出、追蹤與效能測試。'},{title:'從哪裡開始',text:'<code>from ultralytics import YOLO</code><br>讀 README、cfg 與對應任務入口。<br>AGPL-3.0；公開行為以當前版本為準。'}]),point:'任務與模式是兩個維度；並非所有模型都支援全部組合。',detail:'來源：AGENTS.md、ultralytics/__init__.py、ultralytics/cfg/__init__.py。',instruction:'先解釋模型要回答的問題，再說明可以對模型做哪些操作。'},
  {id:'owners',section:'02 / 架構',title:'共用流程在 engine，任務差異在 models',lead:'這是責任分工，不是每次操作必經的單一路徑。',art:deck.cards('owners',[{title:'入口與設定',text:'<code>cfg/</code>：CLI、參數與模型設定。<br><code>engine/model.py</code>：公開操作入口。'},{title:'流程與任務',text:'<code>engine/</code>：train、val、predict、export 共用流程。<br><code>models/</code>：任務 Trainer／Validator／Predictor。'},{title:'資料與執行',text:'<code>data/</code>：載入與增強。<br><code>nn/</code>：網路與後端。<br><code>utils/</code>：損失、指標、繪圖。'}]),point:'修正放在控制該行為的模組；擴充任務用既有 hooks，避免複製整條迴圈。',instruction:'以推論為例，從 Model.predict 指向共用 Predictor，再看任務後處理。'},
  {id:'needs',section:'03 / 需求地圖',title:'選一個目標，找到入口與驗證方法',lead:'「貢獻調查」是待驗證方向，不是官方待辦或已確認 bug。',art:'<div class="um-needs" data-key="needs"><div class="um-toolbar"><label>搜尋需求／路徑<input type="search" placeholder="例如 classify、資料、engine"></label><label>需求類型<select><option value="">全部</option><option>使用能力</option><option>維護入口</option><option>貢獻調查</option></select></label><button data-clear>清除條件</button></div><div class="um-panes"><div class="um-list"></div><section class="um-detail" aria-label="需求詳情" aria-live="polite"></section></div></div>',previewArt:preview,mount:mountNeeds,point:'需求價值、可重現證據與測試缺口，必須一起判斷。',instruction:'選分類裁切，再看入口、驗證方法與 Codecov。示範搜尋與分類篩選。'},
  {id:'test-map',section:'04 / 深度測試地圖',title:'哪些檔案好改？哪些測試值得補？',lead:'修改難度看影響面；補測試難度看可控輸入、斷言與環境。兩者分開評估。',art:`<div class="um-tests" data-key="test-map"><div class="um-toolbar"><label>搜尋路徑／函式<input data-filter="query" type="search" placeholder="例如 activation、get_cdn_group"></label><label>模組<select data-filter="module"><option value="">全部模組</option>${[...new Set(testAtlas.files.map(f=>f.module))].map(m=>`<option>${m}</option>`).join('')}</select></label><label>修改難度<select data-filter="change"><option value="">全部</option>${difficulty.map(x=>`<option>${x}</option>`).join('')}</select></label><label>補測試難度<select data-filter="test"><option value="">全部</option>${difficulty.map(x=>`<option>${x}</option>`).join('')}</select></label><label>覆蓋率<select data-filter="cov"><option value="">全部</option><option value="missing">有未覆蓋行</option><option value="low">低於 50%</option><option value="absent">報告未收錄</option></select></label><label>調查範圍<select data-filter="review"><option value="reviewed">已逐檔深讀</option><option value="">全部 Python 檔</option></select></label><label>排序<select data-filter="sort"><option value="feasible">測試較易 → 漏行較多</option><option value="misses">未覆蓋行最多</option><option value="coverage">覆蓋率最低</option><option value="path">檔案路徑</option></select></label><button data-clear>清除條件</button></div><p class="um-count" role="status"></p><div class="um-panes"><div class="um-list" aria-label="檔案清單"></div><section class="um-detail" aria-label="測試檔案詳情" aria-live="polite"></section></div></div>`,previewArt:testsPreview,mount:mountTests,point:'容易：固定 CPU／暫存輸入可驗；中等：需模型、狀態或整合；困難：硬體、分散式、外部服務或數值語義。逐檔理由優先於標籤。',detail:`實讀 ${reviewedFiles.length} 檔，其餘明示未評估。覆蓋快照 ${testAtlas.coverageCommit.slice(0,8)}；本機 ${testAtlas.head.slice(0,8)}，逐檔核對內容。`,instruction:'篩選「補測試容易」和「有未覆蓋行」，讀具體測例，再展開未覆蓋函式核對。切換困難檔比較硬體及影響面。'},
  {id:'tree',section:'05 / REPO 目錄',title:'沿目錄下鑽，展開真正的檔案評估',lead:'比照 PySpark 的檔案卡片：起讀符號、測試與下一站；加上實際覆蓋率與難度。',art:'<div class="um-tree" data-key="tree"><div class="um-toolbar"><label>全圖搜尋<input type="search" placeholder="例如 engine、docs、測試"></label><label>閱讀級別<select><option value="">全部</option><option>深入讀</option><option>會操作</option><option>按需追</option></select></label><button data-clear>清除條件</button><button data-up>← 上層</button></div><div class="um-crumbs" aria-label="目錄路徑"></div><div class="um-panes"><div class="um-list"></div><section class="um-detail" aria-label="目錄詳情"></section></div></div>',previewArt:testsPreview,mount:mountTree,point:'展開卡片不切目錄；「下一站」才前往測試地圖。原碼及 Codecov 連結需網路，資料瀏覽可離線。',detail:'52 個目錄節點；測試頁索引全部套件 Python 檔，不受目錄顯示深度限制。',instruction:'進入 ultralytics → engine，展開 results.py；點下一站，在測試地圖查看漏行與斷言。'},
  {id:'coverage',section:'06 / CODECOV',title:'低覆蓋率指出驗證缺口，不能證明功能有錯',lead:'整體 63.19% · 19,429 / 30,746 行 · 未覆蓋 11,317 行',art:`<div class="um-coverage" data-key="coverage">${coverage.map(r=>`<a href="${cc+encodeURIComponent('ultralytics/'+r[0])}" target="_blank" rel="noopener"><b>${r[0]}</b><span class="um-bar"><i style="width:${pct(r)}%"></i></span><strong>${pct(r)}%</strong><small>${r[1]-r[2]} 行未覆蓋</small></a>`).join('')}</div>`,point:'主 CPU suite 預設排除 slow、只選 base export；GPU／ROCm／隔離匯出環境另跑。Callbacks 不收集；執行過不代表有正確斷言。',detail:`<a href="${cc}ultralytics" target="_blank" rel="noopener">Codecov 來源</a>：main 報告 bb3e155，查核 2026-10-28；本機 ${testAtlas.head.slice(0,8)}；216 個報告檔已逐檔確認與快照原碼一致，仍非本機執行結果。`,instruction:'比較 models 的未覆蓋行量與 optim 的低百分比。強調測試報告的環境與範圍會影響結果。'},
  {id:'contribute',section:'07 / 下一步',title:'把需求縮成一條可驗證的改動',lead:'研究地圖負責帶路；選題後才進行實際重現。',art:deck.cards('next',[{title:'01 確認問題',text:'記錄版本、輸入、預期與實際結果。<br>查最新 issue／PR，排除已解決或重複工作。'},{title:'02 找最小修正',text:'搜尋 owner 與所有呼叫者。<br>優先刪除或修改既有路徑，保留驗證與錯誤處理。'},{title:'03 驗證再提交',text:'跑相關既有檢查與真實環境。<br>模型測試使用 scratch cwd 與專用權重目錄，注意 conftest 清理。'}]),point:'本次製作地圖，沒有執行模型測試，也沒有確認新的 production bug。',detail:'參考：AGENTS.md、research/contributing/docs/codebase-map.md 與 roadmap.md。',instruction:'請讀者在需求頁選一題，留下版本、重現命令與停止條件，再開始修改。'},
  deck.end({title:'帶著一個需求，回到地圖',instruction:'回到需求地圖，從一條具體路線開始。'})
]};
