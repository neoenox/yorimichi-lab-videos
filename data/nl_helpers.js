window.NL = {
  async todo(){ if(!window.__todo){ window.__todo = await (await fetch('http://127.0.0.1:8765/nolong_studio_todo.json')).json(); } return window.__todo; },
  setText(el, text){ el.focus(); document.execCommand('selectAll'); document.execCommand('insertText', false, text); el.dispatchEvent(new Event('input', {bubbles:true})); },
  async fill(slug){
    const t = (await this.todo()).find(x => x.slug === slug);
    const tb = document.querySelector('#title-textarea #textbox'); this.setText(tb, t.title);
    const db = document.querySelector('#description-textarea #textbox'); this.setText(db, t.desc);
    document.querySelector('[name=VIDEO_MADE_FOR_KIDS_NOT_MFK]').click();
    return JSON.stringify({title: tb.innerText.slice(0,50), descLen: db.innerText.length});
  },
  next(){ const b = document.querySelector('#next-button'); b.click(); return 'next'; },
  info(){ return document.body.innerText.replace(/\s+/g,' ').slice(0,300); }
};
'helpers ok'
