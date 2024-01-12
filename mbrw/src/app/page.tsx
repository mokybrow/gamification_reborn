import Image from 'next/image'
import styles from './page.module.css'

export default function Home() {
  return (
    <main className={styles.main}>
      <div className={styles.maingrid}>
        <div>
          <span className={styles.mainheader}>
            Ближайшие релизы
          </span>
          <span className={styles.mainheader}>
            Сейчас Играют
          </span>
          <span className={styles.mainheader}>
            Новости
          </span>
          <span className={styles.mainheader}>
            Популярные плейлисты
          </span>
        </div>
        <div>
          <span className={styles.minorheader}>
            События
          </span>
          <p>
            9 Декабря состоится новый сезон фортнайт
          </p>
        </div>
      </div>
    </main>


  )
}
