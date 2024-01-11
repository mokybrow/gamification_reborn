"use client"

import Image from "next/image"
import * as gamepad from '@/static/gamepad.png';
import * as cup from '@/static/cup.png';
import * as calendar from '@/static/calendar.png';
import * as feed from '@/static/feed.png';
import * as playlist from '@/static/playlist.png';

import styles from './navbar.module.css'
import Link from "next/link";


const Navbar = () => {
    return (
        <div className={styles.container}>
            <ul className={styles.navbar}>
                <li>
                    <Link href={"/games"}>
                        <Image src={gamepad} alt={"dev logo"} width={24} height={24} />
                        Все игры
                    </Link>
                </li>
                <li>
                    <Link href={"/releases"}>
                        <Image src={calendar} alt={"dev logo"} width={24} height={24} />
                        Календарь игр
                    </Link>
                </li>
                <li>
                    <Link href={"goty"}>
                        <Image src={cup} alt={"dev logo"} width={24} height={24} />
                        Игры года
                    </Link>
                </li>
                <li>
                    <Link href={"feed"}>
                        <Image src={feed} alt={"dev logo"} width={24} height={24} />
                        Лента новостей
                    </Link>
                </li>
                <li>
                    <Link href={"playlists"}>
                        <Image src={playlist} alt={"dev logo"} width={24} height={24} />
                        Плейлисты
                    </Link>
                </li>
            </ul>
        </div>
    )
}

export default Navbar
