summarize_article = "Schreibe eine Zusammenfassung auf Basis des Artikels"

summarize_news = "Du bist Chefredakteur einer deutschen Tageszeitung. In deinem Daily Newsletter an die Leser gehst auf die Themen des Tages ein. Erwähne die Zahl in eckigen Klammern. Das Format muss so aussehen. [1234]"

def getPromptWithContext(question,context):
  prompt = f"Beantworte die Anfrage und nutze dazu den folgenden Context, wenn du die Anfrage nicht auf Basis des Contexts beantworten kannst, antworte mit Ich weiss es nicht! Anfrage: {question} \n Context: {context}"
  return prompt
#def relevance_message(rss_feed):
  #prompt = f"Ich bin männlich, 48 Jahre alt und interessiere mich für Weltgeschehen, Technik, Finanzen, FCBayern, Bitcoin und Fussball. \n RSS Feed Daten: {rss_feed}. Liefere die Daten auschließlich als Array (ohne jeglichen Kommentar) zurück, dass per Script weiterverarbeitet werden kann und für jedes Element ausschließlich die Relevanz enthält. Die Rückmeldung muss also zwingend in dieser Form erfolgen:[3,6,8,7]"

  #system_message = "Du erhälst Informationen zu einem Nutzerprofil und bist in der Lage die Nachrichten in Form eines RSS-Feeds nach Relevanz zu bewerten.Die Relevanz geht von 1 - nicht relevant bis zu 10 sehr relevant."

  #return system_message,prompt

#def category_message(rss_feed,categories):
#  system_message ="Du bist Redakteur bei der Süddeutschen Zeitung"
#  prompt = f'Du erhälst ein Array von RSS Feed Daten. Deine Aufgabe ist die Zuordnung der einzelnen Nachrichten in Kategorien. Folgende Kategorien sind möglich: {categories}. Liefere ein Array das per Script weiterverarbeitet werden kann und für jedes Element in den RSS Feed Daten ausschließlich die Kategorie in Form einer Zahl enthält.Wenn keine Kategorie passt, benutze die Kategorie Diverses. Die Zahl entspricht dem Index der Kategorien. Die Rückmeldung darf nur ein einfaches Array sein und ausschließlich diesem Muster entsprechen: [0,2,4,1].RSS Feed Daten: {rss_feed}'
#  return prompt,system_message

def write_new_prompt():
  write_new_system_message = f"Du bist Redakteur bei der Süddeutschen Zeitung. Du schreibst hervorragende Texte."
  write_new_prompt ="Schreib einen neuen Artikel auf Basis des mitgelieferten Textes. Behalte unbedingt den ursprünglichen Sinn bei und halte dich zwingend an die Fakten des Textes. Entferne nur dann Dinge wenn diese absolute unrelevant sind. z.B. Headline, Author, Datum und Zeit. Hier der Text: "
  return (write_new_system_message,write_new_prompt)

