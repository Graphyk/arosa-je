<script lang="ts">
    import type { iconProps } from ".";

    let {
        color,
        size = 20
    }: iconProps = $props()
</script>

<svg width={size} height={size} viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M10.0003 2.30295V1.73279M10.0003 18.2674V17.6972M17.6974 10.0001H18.2676M1.73303 10.0001H2.30319M15.4435 4.55745L15.8467 4.15429M4.15393 15.8459L4.55709 15.4427M15.4435 15.4427L15.8467 15.8459M4.15393 4.15424L4.55709 4.55741M14.5504 9.96889C14.5504 12.488 12.5083 14.5302 9.98918 14.5302C7.47007 14.5302 5.42792 12.488 5.42792 9.96889C5.42792 7.44978 7.47007 5.40763 9.98918 5.40763C12.5083 5.40763 14.5504 7.44978 14.5504 9.96889Z" stroke={color} stroke-width="2" stroke-linecap="round"/>
</svg>