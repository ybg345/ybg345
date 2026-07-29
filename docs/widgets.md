# Widget Fallback URLs

Third-party README widgets can break when public services hit GitHub API rate limits. If a widget shows a broken image or error message, try these verified alternatives.

## GitHub Stats & Top Languages

**Primary:** `github-stats-extended.vercel.app`

```
https://github-stats-extended.vercel.app/api?username=maf345
https://github-stats-extended.vercel.app/api/top-langs/?username=maf345
```

## GitHub Streak

**Primary:** `github-readme-streak-stats-eight.vercel.app`

**Fallback:** `github-readme-streak-stats-two.vercel.app` or `streak-stats.demolab.com`

```
https://github-readme-streak-stats-eight.vercel.app/?user=maf345
https://github-readme-streak-stats-two.vercel.app/?user=maf345
https://streak-stats.demolab.com/?user=maf345
```

If you see **"Failed to retrieve contributions"**, the public instance is rate-limited. Switch to another mirror above or self-host on Vercel with a GitHub token.

## GitHub Trophies

**Primary:** `github-profile-trophy-sigma-eight.vercel.app`

**Avoid (dead):** `github-profile-trophy-sigma-one.vercel.app` (404)

```
https://github-profile-trophy-sigma-eight.vercel.app/?username=maf345
```

## Badge Layout

GitHub may render external SVG badges as block elements (one per line). Use HTML `<table>` rows with one badge per `<td>` for reliable inline layout.

To stretch badge tables to full profile width, add an invisible spacer row (GitHub ignores `width="100%"` on tables):

```html
<tr>
  <td colspan="10"><img width="1200" height="0" alt="" /></td>
</tr>
```

## Languages Card

To hide languages that don't represent your core work (e.g. HTML exports or Jupyter Notebook analysis repos):

```
&hide=HTML,Jupyter%20Notebook
```
